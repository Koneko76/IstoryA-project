from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import createStory, CreateUserForm, createStoryHome, regenerateStoryHome, validationStoryHome, saveStoryboard, ChangeNameStoryboard, PublishStoryboard
import gpt_2_simple as gpt2
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import tensorflow as tf
import re
from main.models import storyboard, storyboard_text, storyboard_publications, storyboard_picture
from django.utils import timezone
from django.contrib.auth.models import User
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

fs = FileSystemStorage()
path = fs.path("main/static/main/checkpoint")

def remove_last_sentence(text):
    text = text.split(".")
    del text[-1]
    text = ".".join(text)
    text = text + "."
    return text

def index(request):
    form = createStory(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data["startStory"])
        print(form.cleaned_data["typeStory"])
        genre = form.cleaned_data["typeStory"]
        if genre == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif genre == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-fantasy-124M"

        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=form.cleaned_data["startStory"], return_as_list=True, length=512)[0]
        result = remove_last_sentence(result)
        return render(request, 'main/first_text_generation.html', locals())

    template = loader.get_template('main/index.html')
    return render(request, 'main/index.html', locals())


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'main/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def homePage(request):
    form = createStoryHome(request.POST or None)
    formValidation = validationStoryHome(request.POST or None)
    formNext = saveStoryboard(request.POST or None)

    count_storyboard = storyboard.objects.filter(owner_id=request.user.id)

    if form.is_valid():
        lengthStory = form.cleaned_data["lengthStory"]
        if(lengthStory > 512):
            lengthStory = 512;
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        genre = form.cleaned_data["typeStory"]
        if genre == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif genre == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-fantasy-124M"

        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=form.cleaned_data["startStory"], return_as_list=True , length=lengthStory)[0]
        print(result_text_generation)
        result_text_generation = remove_last_sentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        request.session['start_text_generation'] = form.cleaned_data["startStory"]
        return render(request, 'main/validation.html', locals())

    if formValidation.is_valid():
        lengthStory = formValidation.cleaned_data["lengthStoryValidation"]
        if(lengthStory > 512):
            lengthStory = 512;
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        genre = formValidation.cleaned_data["typeStoryValidation"]
        if genre == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif genre == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-fantasy-124M"

        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formValidation.cleaned_data["startStoryValidation"], return_as_list=True , length=lengthStory)[0]
        print(result_text_generation)
        result_text_generation = remove_last_sentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        request.session['start_text_generation'] = formValidation.cleaned_data["startStoryValidation"]
        return render(request, 'main/validation.html', locals())

    if formNext.is_valid():
        nameStory = formNext.cleaned_data["nameStory"]
        lengthStoryboard = formNext.cleaned_data["lengthStoryboard"]
        if(lengthStoryboard > 12):
            lengthStoryboard = 12;
        result_text_generation = request.session.get('result_text_generation')
        start_text_generation = request.session.get('start_text_generation')
        current_user = request.user
        newStoryboard = storyboard(name=nameStory, length=lengthStoryboard, initial_text=result_text_generation, last_text=result_text_generation, start_text=start_text_generation, owner_id=request.user.id, creation_date=timezone.now(), update_date=timezone.now())
        newStoryboard.save()
        storyboard_infos = storyboard.objects.filter(name=nameStory, owner_id=request.user.id).order_by('-id')[0]
        path_render = '/create/' + str(storyboard_infos.id)
        return redirect(path_render)

    return render(request, 'main/home.html', locals())

def createPage(request, id):

    form = createStoryHome(request.POST or None)
    formRegenerate = regenerateStoryHome(request.POST or None)

    listChoice = 1

    list_save_text = []
    list_all_text = []
    list_save_text_case = []
    list_save_text_id = []
    list_tmp = []
    list_save_picture_case = []
    list_save_picture = []

    storyboard_infos = storyboard.objects.get(id=id, owner_id=request.user.id)
    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=storyboard_infos.id).order_by('case_id', 'text_order')
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)
        list_save_text_case.append(storyboard_text_infos_unit.case_id)
        list_save_text_id.append(storyboard_text_infos_unit.id)

    storyboard_pictures_infos = storyboard_picture.objects.filter(storyboard_id=id)
    for storyboard_pictures_infos_unit in storyboard_pictures_infos:
        list_save_picture.append(storyboard_pictures_infos_unit.picture)
        list_save_picture_case.append(storyboard_pictures_infos_unit.case_id)

    list_picture_save_and_case_id = zip(list_save_picture_case, list_save_picture)
    list_picture_save_and_case_id = dict(list_picture_save_and_case_id)

    result_text_generation = storyboard_infos.last_text
    lengthStoryboard = range(1, storyboard_infos.length+1)
    request.session['result_text_generation'] = result_text_generation
    list_generation_text = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result_text_generation)
    list_all_text = []
    list_all_text = list_save_text + list_generation_text
    #list_all_text_final = []
    #for i in list_all_text:
    #    if i not in list_all_text_final: list_all_text_final.append(i)
    #request.session['result_text_generation_list'] = list_all_text_final
    #list_id_text = range(1, len(list_all_text_final)+1)
    list_save_text_id_length = range(1, len(list_save_text_id)+1)
    list_id_text_save = range(1, len(list_save_text_case)+1)
    #list_text_and_id = [list(i) for i in zip(list_all_text_final, list_id_text)]
    list_text_save_and_id = zip(list_save_text_case, list_id_text_save)
    dict_text = dict()

    for case in range(1, 13):
        dict_text[case] = []

    for length in range(1,13):
        for case, id_text in zip(list_save_text_case, list_id_text_save):
            if length == case:
                dict_text[case].append(id_text)

    update_path = "/update_storyboard/" + str(id)
    overview_path = "/storyboard/" + str(id)
    order_path = "/order_storyboard/" + str(id)

    if form.is_valid():
        lengthStory = form.cleaned_data["lengthStory"]
        if(lengthStory > 512):
            lengthStory = 512;
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        genre = form.cleaned_data["typeStory"]
        if genre == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif genre == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-fantasy-124M"

        print(path_run)
        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=form.cleaned_data["startStory"], return_as_list=True , length=lengthStory)[0]
        print(result_text_generation)
        result_text_generation = remove_last_sentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        list_generation_text = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result_text_generation)
        list_all_text = []
        list_all_text = list_save_text + list_generation_text
        list_all_text_final = []
        for i in list_all_text:
            if i not in list_all_text_final: list_all_text_final.append(i)
        request.session['result_text_generation_list'] = list_all_text_final
        list_id_text = range(1, len(list_all_text_final))
        list_text_and_id = [list(i) for i in zip(list_all_text_final, list_id_text)]
        return render(request, 'main/validation.html', locals())

    if formRegenerate.is_valid():
        lengthStory = formRegenerate.cleaned_data["regenerateLengthStory"]
        if(lengthStory > 512):
            lengthStory = 512;
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        genre = formRegenerate.cleaned_data["regenerateTypeStory"]
        if genre == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif genre == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-fantasy-124M"

        print(path_run)
        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formRegenerate.cleaned_data["regenerateStartStory"], return_as_list=True , length=lengthStory)[0]
        print(result_text_generation)
        result_text_generation = remove_last_sentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        list_generation_text = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result_text_generation)
        list_all_text = []
        list_all_text = list_save_text + list_generation_text
        list_all_text_final = []
        for i in list_all_text:
            if i not in list_all_text_final: list_all_text_final.append(i)
        request.session['result_text_generation_list'] = list_all_text_final
        list_id_text = range(1, len(list_all_text_final))
        list_text_and_id = [list(i) for i in zip(list_all_text_final, list_id_text)]

        current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
        current_storyboard.last_text = result_text_generation
        current_storyboard.update_date = timezone.now()
        current_storyboard.save()

        return render(request, 'main/create.html', locals())

    return render(request, 'main/create.html', locals())

def createOrderPage(request, id):

    form = createStoryHome(request.POST or None)
    formRegenerate = regenerateStoryHome(request.POST or None)

    list_save_text = []
    list_all_text = []
    list_save_text_case = []
    list_save_text_id = []
    list_tmp = []
    list_save_picture_case = []
    list_save_picture = []

    storyboard_infos = storyboard.objects.get(id=id, owner_id=request.user.id)
    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=storyboard_infos.id).order_by('case_id', 'text_order')
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)
        list_save_text_case.append(storyboard_text_infos_unit.case_id)
        list_save_text_id.append(storyboard_text_infos_unit.id)

    storyboard_pictures_infos = storyboard_picture.objects.filter(storyboard_id=id)
    for storyboard_pictures_infos_unit in storyboard_pictures_infos:
        list_save_picture.append(storyboard_pictures_infos_unit.picture)
        list_save_picture_case.append(storyboard_pictures_infos_unit.case_id)

    list_picture_save_and_case_id = zip(list_save_picture_case, list_save_picture)
    list_picture_save_and_case_id = dict(list_picture_save_and_case_id)

    result_text_generation = storyboard_infos.last_text
    lengthStoryboard = range(1, storyboard_infos.length+1)
    request.session['result_text_generation'] = result_text_generation
    list_generation_text = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result_text_generation)
    list_all_text = []
    list_all_text = list_save_text + list_generation_text
    list_all_text_final = []
    for i in list_all_text:
        if i not in list_all_text_final: list_all_text_final.append(i)
    request.session['result_text_generation_list'] = list_all_text_final
    list_id_text = range(1, len(list_all_text_final)+1)
    list_save_text_id_length = range(1, len(list_save_text_id)+1)
    list_id_text_save = range(1, len(list_save_text_case)+1)
    list_text_and_id = [list(i) for i in zip(list_all_text_final, list_id_text)]
    list_text_save_and_id = zip(list_save_text_case, list_id_text_save)
    dict_text = dict()

    for case in range(1, 13):
        dict_text[case] = []

    for length in range(1,13):
        for case, id_text in zip(list_save_text_case, list_id_text_save):
            if length == case:
                dict_text[case].append(id_text)

    update_path = "/update_storyboard/" + str(id)
    overview_path = "/storyboard/" + str(id)
    create_path = "/create/" + str(id)

    if form.is_valid():
        lengthStory = form.cleaned_data["lengthStory"]
        if(lengthStory > 512):
            lengthStory = 512;
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        genre = form.cleaned_data["typeStory"]
        if genre == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif genre == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-fantasy-124M"

        print(path_run)
        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=form.cleaned_data["startStory"], return_as_list=True , length=lengthStory)[0]
        print(result_text_generation)
        result_text_generation = remove_last_sentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        list_generation_text = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result_text_generation)
        list_all_text = []
        list_all_text = list_save_text + list_generation_text
        list_all_text_final = []
        for i in list_all_text:
            if i not in list_all_text_final: list_all_text_final.append(i)
        request.session['result_text_generation_list'] = list_all_text_final
        list_id_text = range(1, len(list_all_text_final))
        list_text_and_id = [list(i) for i in zip(list_all_text_final, list_id_text)]
        return render(request, 'main/validation.html', locals())

    if formRegenerate.is_valid():
        lengthStory = formRegenerate.cleaned_data["regenerateLengthStory"]
        if(lengthStory > 512):
            lengthStory = 512;
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        genre = formRegenerate.cleaned_data["regenerateTypeStory"]
        if genre == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif genre == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-fantasy-124M"

        print(path_run)
        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formRegenerate.cleaned_data["regenerateStartStory"], return_as_list=True , length=lengthStory)[0]
        print(result_text_generation)
        result_text_generation = remove_last_sentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        list_generation_text = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result_text_generation)
        list_all_text = []
        list_all_text = list_save_text + list_generation_text
        list_all_text_final = []
        for i in list_all_text:
            if i not in list_all_text_final: list_all_text_final.append(i)
        request.session['result_text_generation_list'] = list_all_text_final
        list_id_text = range(1, len(list_all_text_final))
        list_text_and_id = [list(i) for i in zip(list_all_text_final, list_id_text)]

        current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
        current_storyboard.last_text = result_text_generation
        current_storyboard.update_date = timezone.now()
        current_storyboard.save()

        return render(request, 'main/create2.html', locals())
    return render(request, 'main/create2.html', locals())

def updateStoryboard(request, id):

    result_text_generation = request.session.get('result_text_generation')
    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    current_storyboard.last_text = result_text_generation
    current_storyboard.update_date = timezone.now()
    current_storyboard.save()

    path_render = "/create/" + str(id)
    return redirect(path_render)

def viewStoryboard(request, id):

    list_save_text_case = []
    list_save_text = []
    list_save_picture_case = []
    list_save_picture = []

    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    current_storyboard_length = current_storyboard.length
    current_storyboard_length = range(1, current_storyboard_length+1)
    current_storyboard_nb_picture = current_storyboard.length

    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=current_storyboard.id)
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)
        list_save_text_case.append(storyboard_text_infos_unit.case_id)

    storyboard_pictures_infos = storyboard_picture.objects.filter(storyboard_id=current_storyboard.id)
    for storyboard_pictures_infos_unit in storyboard_pictures_infos:
        list_save_picture.append(storyboard_pictures_infos_unit.picture)
        list_save_picture_case.append(storyboard_pictures_infos_unit.case_id)

    list_text_save_and_case_id = zip(list_save_text_case, list_save_text)
    list_text_save_and_case_id = dict(list_text_save_and_case_id)

    list_picture_save_and_case_id = zip(list_save_picture_case, list_save_picture)
    list_picture_save_and_case_id = dict(list_picture_save_and_case_id)

    list_id_text_save = range(1, len(list_save_text_case) + 1)

    dict_text = dict()
    for case in range(1, 13):
        dict_text[case] = []

    for length in range(1, 13):
        for case, text in zip(list_save_text_case, list_save_text):
            if length == case:
                dict_text[case].append(text)

    formChangeName = ChangeNameStoryboard(request.POST or None)
    formPublishStoryboard = PublishStoryboard(request.POST or None)

    if formChangeName.is_valid():
        current_storyboard.name = formChangeName.cleaned_data["newNameStoryboard"]
        current_storyboard.save()

        path_render = "/storyboard/" + str(current_storyboard.id)
        return redirect(path_render)

    if formPublishStoryboard.is_valid():
        current_storyboard.publish_statut = 1
        current_storyboard.message = formPublishStoryboard.cleaned_data["messagetoryboard"]
        current_storyboard.date_publish = timezone.now()
        current_storyboard.save()

        path_render = "/storyboard/" + str(current_storyboard.id)
        return redirect(path_render)

    update_storyboard_path = "/create/" + str(current_storyboard.id)
    delete_storyboard_path = "/delete/" + str(current_storyboard.id)
    return render(request, 'main/storyboard.html', locals())

def deleteStoryboard(request, id):

    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    current_storyboard.delete()
    return redirect("/home")

def UpdateCaseStoryboard(request):

    result_text_generation_list = request.session.get('result_text_generation_list')
    n_case = request.POST.get("n_case")
    n_text = request.POST.get("n_text")
    n_storyboard = request.POST.get("n_storyboard")
    current_storyboard = storyboard.objects.get(id=n_storyboard, owner_id=request.user.id)

    print("case ", n_case)

    try:
        existStoryboardText = storyboard_text.objects.get(storyboard_id=current_storyboard.id, text=result_text_generation_list[int(n_text)-1], owner_id=request.user.id)
        existStoryboardText.case_id = n_case
        existStoryboardText.text_order = 100
        existStoryboardText.save()
    except:
        newStoryboardText = storyboard_text(storyboard=current_storyboard, case_id=n_case, text=result_text_generation_list[int(n_text)-1], owner_id=request.user.id)
        newStoryboardText.save()

    return HttpResponse({"operation_result": "ok"})

def UpdateCaseOrderStoryboard(request):

    storyboard_id = request.POST.get("storyboard_id")
    case_id = request.POST.get("case_id")
    text_order = int(request.POST.get("text_order")) + 1
    text = request.POST.get("text")

    newStoryboardTextOrder = storyboard_text.objects.get(text=str(text), storyboard_id=storyboard_id, case_id=case_id, owner_id=request.user.id)
    newStoryboardTextOrder.text_order = text_order
    newStoryboardTextOrder.save()

    response_data = {}
    response_data['result'] = "ok"

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def favStoryboardHome(request, id):

    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    if(current_storyboard.owner_fav == 0):
        current_storyboard.owner_fav = 1
    else:
        current_storyboard.owner_fav = 0
    current_storyboard.save()
    return redirect("/home")

def wallPage(request):

    publish_user_infos = []
    publish_like_infos = []
    publish_fav_infos = []

    publish_list_storyboard = storyboard.objects.filter(publish_statut=1)

    for publish_unit in publish_list_storyboard:
        user_infos = User.objects.get(id=publish_unit.owner_id)
        publish_infos_like = storyboard_publications.objects.filter(storyboard=publish_unit.id, fav=1).count()
        publish_infos_fav = storyboard_publications.objects.filter(storyboard=publish_unit.id, like=1).count()
        publish_like_infos.append(publish_infos_like)
        publish_fav_infos.append(publish_infos_fav)
        publish_user_infos.append(user_infos.username)

    test = zip(publish_list_storyboard, publish_user_infos, publish_like_infos, publish_fav_infos)

    return render(request, 'main/wall.html', locals())


def likeStoryboardPublication(request, id):

    current_storyboard = storyboard.objects.get(id=id)
    try:
        storyboard_publication = storyboard_publications.objects.get(owner_id=request.user.id,storyboard=id)
        if(storyboard_publication.like == 1):
            storyboard_publication.like = 0;
            storyboard_publication.save()
        else:
            storyboard_publication.like = 1;
            storyboard_publication.save()
    except:
        storyboard_publication = storyboard_publications(storyboard=current_storyboard, like=1, owner_id=request.user.id)
        storyboard_publication.save()

    return redirect("/wall")


def favStoryboardPublication(request, id):

    current_storyboard = storyboard.objects.get(id=id)
    try:
        storyboard_publication = storyboard_publications.objects.get(owner_id=request.user.id,storyboard=id)
        if(storyboard_publication.fav == 1):
            storyboard_publication.fav = 0;
            storyboard_publication.save()
        else:
            storyboard_publication.fav = 1;
            storyboard_publication.save()
    except:
        storyboard_publication = storyboard_publications(storyboard=current_storyboard, fav=1, owner_id=request.user.id)
        storyboard_publication.save()

    return redirect("/wall")

def indexListCreateStoryboard(request):

    index = request.POST.get("index")
    return HttpResponse({"index_result": index})

def sup(request):

    current_storyboard_text = storyboard_text.objects.get(id=28)
    current_storyboard_text.text = "Victorious, she is able to reach her flower shop."
    current_storyboard_text.save()

    return redirect("/wall")

def getTextByID(request):

    list_text_id = []
    storyboard_id = request.POST.get("storyboard_id")
    text_id = request.POST.get("text_id")
    case_id = request.POST.get("case_id")

    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=storyboard_id, owner_id=request.user.id).order_by('case_id', 'text_order')
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_text_id.append(storyboard_text_infos_unit.id)

    text_id_final = list_text_id[int(text_id) - 1]
    newStoryboardTextOrder = storyboard_text.objects.get(id=text_id_final, storyboard_id=storyboard_id, case_id=case_id, owner_id=request.user.id)
    response_data = {}
    response_data['result'] = newStoryboardTextOrder.text

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def updateListText(request):

    list_save_text = []
    list_index = request.GET.get("list_num")
    id = request.GET.get("storyboard")

    storyboard_infos = storyboard.objects.get(id=id, owner_id=request.user.id)
    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=storyboard_infos.id).order_by('case_id', 'text_order')

    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)

    result_text_generation = storyboard_infos.last_text
    request.session['result_text_generation'] = result_text_generation
    list_generation_text = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", result_text_generation)
    list_all_text = list_save_text + list_generation_text
    list_all_text_final = []
    for i in list_all_text:
        if i not in list_all_text_final: list_all_text_final.append(i)
    request.session['result_text_generation_list'] = list_all_text_final
    list_id_text = range(1, len(list_all_text_final) + 1)
    list_text_and_id = [list(i) for i in zip(list_all_text_final, list_id_text)]

    if(int(list_index) == 1):
        list_text_and_id = list_text_and_id[0:len(list_save_text)]
        return render(request, 'main/list_text.html', locals())
    if(int(list_index) == 2):
        list_text_and_id = list_text_and_id[len(list_save_text):]
        return render(request, 'main/list_text.html', locals())

    return render(request, 'main/list_text.html', locals())

def updateListPicture(request):

    list_save_picture_case = []
    list_save_picture = []
    id = request.GET.get("storyboard")

    storyboard_pictures_infos = storyboard_picture.objects.filter(storyboard_id=id)
    for storyboard_pictures_infos_unit in storyboard_pictures_infos:
        list_save_picture.append(storyboard_pictures_infos_unit.picture)
        list_save_picture_case.append(storyboard_pictures_infos_unit.case_id)

    list_picture_save_and_case_id = zip(list_save_picture_case, list_save_picture)
    list_picture_save_and_case_id = dict(list_picture_save_and_case_id)

    return render(request, 'main/update_picture.html', locals())

def createPicture(request):

    storyboard_id = request.POST.get("storyboard_id")
    case_id = request.POST.get("case_id")
    text = request.POST.get("text")
    current_storyboard = storyboard.objects.get(id=storyboard_id)

    try:
        current_storyboard_picture = storyboard_picture.objects.get(storyboard=current_storyboard, case_id=case_id, owner_id=request.user.id)
        current_storyboard_picture.text = text
        current_storyboard_picture.save()
    except:
        current_storyboard_picture = storyboard_picture(storyboard=current_storyboard, case_id=case_id, text=text, owner_id=request.user.id)
        current_storyboard_picture.save()

    return HttpResponse({"operation_result": "ok"})

@csrf_exempt
def updatePictureByFlask(request):

    storyboard_id = request.POST.get("storyboard_id")
    case_id = request.POST.get("case_id")
    owner_id = request.POST.get("owner_id")
    pictureB64 = request.POST.get("pictureB64")
    current_storyboard = storyboard.objects.get(id=storyboard_id)

    print("storyboard_id", storyboard_id, "case_id", case_id, "owner_id", owner_id, "pictureB64", pictureB64)

    current_storyboard_picture = storyboard_picture.objects.get(storyboard=current_storyboard, case_id=case_id, owner_id=owner_id)
    current_storyboard_picture.picture = BytesIO(base64.b64decode(pictureB64)).read()
    current_storyboard_picture.save()

    return HttpResponse({"operation_result": "ok"})
