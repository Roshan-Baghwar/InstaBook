from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
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

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, username=username, name=firstName+' '+lastName, mobile=mobile, email=email)
                new_profile.save()
                messages.info(request, 'Sign Up Successful!')
                return redirect('signup')

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

# api /logout
def logout(request):
    auth.logout(request)
    return redirect('signin')