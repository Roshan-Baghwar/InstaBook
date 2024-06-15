from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from itertools import chain
from InstaBookApplication.models import Profile, Post, LikePost, Follow


def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    feed_post = Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'feed_post':feed_post})

# api /signup
def signup(request):

    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        username = request.POST['username']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Exists')
                return redirect('signup')
            elif User.objects.filter(id=mobile).exists():
                messages.info(request, 'Mobile Already Exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, id=mobile, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, username=username, firstName=firstName, lastName=lastName, mobile=mobile, email=email)
                new_profile.save()
                # messages.info(request, 'Sign Up Successful!')
                return redirect('settings')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
# api /signin
def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
        
    else:   
        return render(request, 'signin.html')

# api /settings
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('image')
        if request.POST['firstName'] == None:
            firstName = user_profile.firstName
        else:
            firstName = request.POST['firstName']
        if request.POST['lastName'] == None:
            lastName = user_profile.lastName
        else:
            lastName = request.POST['lastName']
        if request.POST['email'] == None:
            email = user_profile.email
        else:
            email = request.POST['email']

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.firstName = firstName
        user_profile.lastName = lastName
        user_profile.email = email
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('settings')


    return render(request, 'setting.html', {'user_profile':user_profile})
    
# api /post
def post(request):

    if request.method == 'POST':
        username = request.user.username
        image = request.FILES.get('post_image')
        caption = request.POST['caption']

        new_post = Post.objects.create(username=username, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    
    else:
        return redirect('/')

# api /like
def likepost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -=1
        post.save()
        return redirect('/')


# api /profile
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(username=pk)
    user_post_length = len(user_post)

    follower = request.user.username
    user = pk

    user_followers = len(Follow.objects.filter(user=pk))
    user_following = len(Follow.objects.filter(follower=pk))

    if Follow.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text= 'Follow'

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_post' : user_post,
        'user_post_length': user_post_length,
        'user_followers' : user_followers,
        'user_following' : user_following,
        'button_text' : button_text
    }
    return render(request, 'profile.html', context)

# api /follow
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Follow.objects.filter(follower=follower, user=user).first():
            delete_follower = Follow.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Follow.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)

    else:
        return redirect('/')

# api /search
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(username=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for id in username_profile:
            profile_lists = Profile.objects.filter(username=id)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
        context = {
            'user_profile' : user_profile,
            'username_profile_list' : username_profile_list
        }
    return render(request, 'search.html', context)
# api /logout
def logout(request):
    auth.logout(request)
    return redirect('signin')