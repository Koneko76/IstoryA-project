from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateStory, CreateUserForm, CreateStoryHome, RegenerateStoryHome, ValidationStoryHome, SaveStoryboard, ChangeNameStoryboard, PublishStoryboard
import gpt_2_simple as gpt2
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import tensorflow as tf
from main.models import storyboard, storyboard_text, storyboard_publications, storyboard_picture
from django.utils import timezone
from django.contrib.auth.models import User
import json
import base64
from io import BytesIO
from nltk.tokenize import sent_tokenize
from fpdf import FPDF
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import textwrap
import os
from main.abstract_generation import generate_abstract

fs = FileSystemStorage()
path = fs.path("main/static/main/checkpoint")

def removeLastSentence(text):
    text = text.split(".")
    del text[-1]
    text = ".".join(text)
    text = text + "."

    return text

def sup():
    current_storyboard_text = storyboard_text.objects.get(id=28)
    current_storyboard_text.text = "Victorious, she is able to reach her flower shop."
    current_storyboard_text.save()

    return redirect("/wall")

def index(request):
    formCreateStory = CreateStory(request.POST or None)

    if formCreateStory.is_valid():
        type = formCreateStory.cleaned_data["type"]

        if type == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif type == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-western-124M"

        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formCreateStory.cleaned_data["start"], return_as_list=True, length=256)[0]
        result = removeLastSentence(result)

        return render(request, 'main/first_text_generation.html', locals())

    return render(request, 'main/index.html', locals())

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        formCreateUser = CreateUserForm()

        if request.method == 'POST':
            formCreateUser = CreateUserForm(request.POST)

            if formCreateUser.is_valid():
                formCreateUser.save()
                return redirect('login')

        context = {'formCreateUser': formCreateUser}
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

@login_required
def logoutUser(request):
    logout(request)

    return redirect('login')

@login_required
def homePage(request):
    formCreateStoryHome = CreateStoryHome(request.POST or None)
    formRegenerateValidation = ValidationStoryHome(request.POST or None)
    formNext = SaveStoryboard(request.POST or None)
    list_storyboard = []
    list_profil_picture = []
    count_storyboard = storyboard.objects.filter(owner_id=request.user.id)

    for storyboard_infos in count_storyboard:
        list_storyboard.append(storyboard_infos.id)

    for current_storyboard in list_storyboard:
        try:
            current_picture = storyboard_picture.objects.get(case_id=1, owner_id=request.user.id, storyboard=current_storyboard)
            if current_picture.picture is None:
                list_profil_picture.append("bear.jpg")
            else:
                list_profil_picture.append(current_picture.picture)
        except:
            list_profil_picture.append("bear.jpg")

    count_storyboard = zip(count_storyboard, list_profil_picture)

    if formCreateStoryHome.is_valid():
        length = formCreateStoryHome.cleaned_data["length"]
        type = formCreateStoryHome.cleaned_data["type"]
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()

        if(length > 256):
            length = 256;

        if type == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif type == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-western-124M"

        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formCreateStoryHome.cleaned_data["start"], return_as_list=True , length=length)[0]
        result_text_generation = removeLastSentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        request.session['start_text_generation'] = formCreateStoryHome.cleaned_data["start"]

        return render(request, 'main/validation.html', locals())

    if formRegenerateValidation.is_valid():
        length = formRegenerateValidation.cleaned_data["length"]
        type = formRegenerateValidation.cleaned_data["type"]
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()

        if(length > 256):
            length = 256;

        if type == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif type == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-western-124M"

        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formRegenerateValidation.cleaned_data["start"], return_as_list=True , length=length)[0]
        result_text_generation = removeLastSentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        request.session['start_text_generation'] = formRegenerateValidation.cleaned_data["start"]

        return render(request, 'main/validation.html', locals())

    if formNext.is_valid():
        name = formNext.cleaned_data["name"]
        length_storyboard = formNext.cleaned_data["length_storyboard"]
        result_text_generation = request.session.get('result_text_generation')
        start_text_generation = request.session.get('start_text_generation')

        if(length_storyboard > 12):
            length_storyboard = 12;

        newStoryboard = storyboard(name=name, length=length_storyboard, initial_text=result_text_generation, last_text=result_text_generation, start_text=start_text_generation, owner_id=request.user.id, creation_date=timezone.now(), update_date=timezone.now())
        newStoryboard.save()

        storyboard_infos = storyboard.objects.filter(name=name, owner_id=request.user.id).order_by('-id')[0]

        path_render = '/create/' + str(storyboard_infos.id)
        return redirect(path_render)

    return render(request, 'main/home.html', locals())

@login_required
def createPage(request, id):
    form = CreateStoryHome(request.POST or None)
    formRegenerate = RegenerateStoryHome(request.POST or None)
    list_save_text = []
    list_save_text_case = []
    list_save_text_id = []
    list_save_picture = []
    list_save_picture_case = []
    list_all_text = []
    list_all_text_final = []
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

    list_id_text_save = range(1, len(list_save_text_case) + 1)
    storyboard_range = range(1, storyboard_infos.length + 1)

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

    if formRegenerate.is_valid():
        regenerate_length = formRegenerate.cleaned_data["regenerate_length"]
        if(regenerate_length > 256):
            regenerate_length = 256;
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()
        regenerate_type = formRegenerate.cleaned_data["regenerate_type"]
        if regenerate_type == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif regenerate_type == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-western-124M"

        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formRegenerate.cleaned_data["regenerate_start"], return_as_list=True , length=regenerate_length)[0]
        result_text_generation = removeLastSentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        list_generation_text = sent_tokenize(result_text_generation)

        list_all_text = list_save_text + list_generation_text
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

@login_required
def createOrderPage(request, id):
    form = CreateStoryHome(request.POST or None)
    formRegenerate = RegenerateStoryHome(request.POST or None)
    list_save_text = []
    list_save_text_case = []
    list_save_text_id = []
    list_save_picture = []
    list_save_picture_case = []
    list_all_text = []
    list_all_text_final = []
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

    list_id_text_save = range(1, len(list_save_text_case) + 1)
    storyboard_range = range(1, storyboard_infos.length + 1)

    dict_text = dict()
    for case in range(1, 13):
        dict_text[case] = []
    for length in range(1,13):
        for case, id_text in zip(list_save_text_case, list_id_text_save):
            if length == case:
                dict_text[case].append(id_text)

    update_path_reorder = "/update_storyboard_reorder/" + str(id)
    overview_path = "/storyboard/" + str(id)
    create_path = "/create/" + str(id)

    if formRegenerate.is_valid():
        regenerate_length = formRegenerate.cleaned_data["regenerate_length"]
        regenerate_type = formRegenerate.cleaned_data["regenerate_type"]
        tf.reset_default_graph()
        sess = gpt2.start_tf_sess()

        if(regenerate_length > 256):
            regenerate_length = 256;

        if regenerate_type == "Fantasy":
            path_run = "run1-fantasy-124M"
        elif regenerate_type == "Romance":
            path_run = "run1-romance-124M"
        else:
            path_run = "run1-western-124M"

        gpt2.load_gpt2(sess, checkpoint_dir=path, run_name=path_run)
        result_text_generation = gpt2.generate(sess, checkpoint_dir=path, run_name=path_run, prefix=formRegenerate.cleaned_data["regenerate_start"], return_as_list=True , length=regenerate_length)[0]
        result_text_generation = removeLastSentence(result_text_generation)
        request.session['result_text_generation'] = result_text_generation
        list_generation_text = sent_tokenize(result_text_generation)

        list_all_text = list_save_text + list_generation_text
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

@login_required
def updateStoryboard(request, id):
    result_text_generation = request.session.get('result_text_generation')

    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    current_storyboard.last_text = result_text_generation
    current_storyboard.update_date = timezone.now()
    current_storyboard.save()

    path_render = "/create/" + str(id)
    return redirect(path_render)

@login_required
def updateReorderStoryboard(request, id):
    result_text_generation = request.session.get('result_text_generation')

    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    current_storyboard.last_text = result_text_generation
    current_storyboard.update_date = timezone.now()
    current_storyboard.save()

    path_render = "/order_storyboard/" + str(id)
    return redirect(path_render)

@login_required
def storyboardPage(request, id):
    formChangeName = ChangeNameStoryboard(request.POST or None)
    formPublishStoryboard = PublishStoryboard(request.POST or None)
    list_save_text_case = []
    list_save_text = []
    list_save_picture_case = []
    list_save_picture = []
    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    length_picture = storyboard_picture.objects.filter(storyboard_id=id, owner_id=request.user.id).count()

    current_storyboard_length = current_storyboard.length
    current_storyboard_range = range(1, current_storyboard_length+1)

    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=current_storyboard.id)
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)
        list_save_text_case.append(storyboard_text_infos_unit.case_id)

    list_text_save_and_case_id = zip(list_save_text_case, list_save_text)
    list_text_save_and_case_id = dict(list_text_save_and_case_id)

    storyboard_pictures_infos = storyboard_picture.objects.filter(storyboard_id=current_storyboard.id)
    for storyboard_pictures_infos_unit in storyboard_pictures_infos:
        list_save_picture.append(storyboard_pictures_infos_unit.picture)
        list_save_picture_case.append(storyboard_pictures_infos_unit.case_id)

    list_picture_save_and_case_id = zip(list_save_picture_case, list_save_picture)
    list_picture_save_and_case_id = dict(list_picture_save_and_case_id)

    dict_text = dict()
    for case in range(1, 13):
        dict_text[case] = []
    for length in range(1, 13):
        for case, text in zip(list_save_text_case, list_save_text):
            if length == case:
                dict_text[case].append(text)

    if formChangeName.is_valid():
        current_storyboard.name = formChangeName.cleaned_data["new_name"]
        current_storyboard.save()

        path_render = "/storyboard/" + str(current_storyboard.id)
        return redirect(path_render)

    if formPublishStoryboard.is_valid():
        current_storyboard.publish_statut = 1
        current_storyboard.publish_message = formPublishStoryboard.cleaned_data["publication_message"]
        current_storyboard.publish_date = timezone.now()
        current_storyboard.save()

        path_render = "/storyboard/" + str(current_storyboard.id)
        return redirect(path_render)

    update_storyboard_path = "/create/" + str(current_storyboard.id)
    delete_storyboard_path = "/delete/" + str(current_storyboard.id)
    generate_pdf_path = "/generate_pdf/" + str(current_storyboard.id)
    generate_abstract_path = "/generate_abstract/" + str(current_storyboard.id)
    return render(request, 'main/storyboard.html', locals())

@login_required
def storyboardPublishedPage(request, id):
    list_save_text = []
    list_save_text_case = []
    list_save_picture = []
    list_save_picture_case = []
    current_storyboard = storyboard.objects.get(id=id)

    current_storyboard_length = current_storyboard.length
    current_storyboard_length = range(1, current_storyboard_length+1)

    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=current_storyboard.id)
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)
        list_save_text_case.append(storyboard_text_infos_unit.case_id)

    list_text_save_and_case_id = zip(list_save_text_case, list_save_text)
    list_text_save_and_case_id = dict(list_text_save_and_case_id)

    storyboard_pictures_infos = storyboard_picture.objects.filter(storyboard_id=current_storyboard.id)
    for storyboard_pictures_infos_unit in storyboard_pictures_infos:
        list_save_picture.append(storyboard_pictures_infos_unit.picture)
        list_save_picture_case.append(storyboard_pictures_infos_unit.case_id)

    list_picture_save_and_case_id = zip(list_save_picture_case, list_save_picture)
    list_picture_save_and_case_id = dict(list_picture_save_and_case_id)

    dict_text = dict()
    for case in range(1, 13):
        dict_text[case] = []
    for length in range(1, 13):
        for case, text in zip(list_save_text_case, list_save_text):
            if length == case:
                dict_text[case].append(text)

    return render(request, 'main/storyboard_published.html', locals())

@login_required
def deleteStoryboard(request, id):
    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)
    current_storyboard.delete()

    return redirect("/home")

@login_required
def updateCaseStoryboard(request):
    result_text_generation_list = request.session.get('result_text_generation_list')
    n_case = request.POST.get("n_case")
    n_text = request.POST.get("n_text")
    n_storyboard = request.POST.get("n_storyboard")
    current_storyboard = storyboard.objects.get(id=n_storyboard, owner_id=request.user.id)

    if(str(n_case) == "generation_depot"):
        current_storyboard_text = storyboard_text.objects.get(storyboard_id=current_storyboard.id,text=result_text_generation_list[int(n_text) - 1],owner_id=request.user.id)
        current_storyboard_text.delete()
    else:
        try:
            current_storyboard_text = storyboard_text.objects.get(storyboard_id=current_storyboard.id, text=result_text_generation_list[int(n_text)-1], owner_id=request.user.id)
            current_storyboard_text.case_id = n_case
            current_storyboard_text.text_order = 100
            current_storyboard_text.save()
        except:
            new_storyboard_text = storyboard_text(storyboard=current_storyboard, case_id=n_case, text=result_text_generation_list[int(n_text)-1], owner_id=request.user.id)
            new_storyboard_text.save()

    return HttpResponse({"operation_result": "ok"})

@login_required
def updateCaseOrderStoryboard(request):
    storyboard_id = request.POST.get("storyboard_id")
    case_id = request.POST.get("case_id")
    text_order = int(request.POST.get("text_order")) + 1
    text = request.POST.get("text")
    response_data = {}

    print(storyboard_id, case_id, text_order, "text", text)

    current_storyboard_text = storyboard_text.objects.get(text=str(text), storyboard_id=storyboard_id, case_id=case_id, owner_id=request.user.id)
    current_storyboard_text.text_order = text_order
    current_storyboard_text.save()

    response_data['result'] = "ok"
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def favStoryboardHome(request, id):
    current_storyboard = storyboard.objects.get(id=id, owner_id=request.user.id)

    if(current_storyboard.owner_fav == 0):
        current_storyboard.owner_fav = 1
    else:
        current_storyboard.owner_fav = 0

    current_storyboard.save()

    return redirect("/home")

@login_required
def wallPage(request):
    publish_user_infos = []
    publish_like_infos = []
    publish_fav_infos = []
    list_storyboard = []
    list_profil_picture = []
    list_storyboard_published = storyboard.objects.filter(publish_statut=1)

    for publish_unit in list_storyboard_published:
        user_infos = User.objects.get(id=publish_unit.owner_id)
        publish_infos_like = storyboard_publications.objects.filter(storyboard=publish_unit.id, fav=1).count()
        publish_infos_fav = storyboard_publications.objects.filter(storyboard=publish_unit.id, like=1).count()
        publish_like_infos.append(publish_infos_like)
        publish_fav_infos.append(publish_infos_fav)
        publish_user_infos.append(user_infos.username)

    infos = zip(list_storyboard_published, publish_user_infos, publish_like_infos, publish_fav_infos, list_profil_picture)

    for storyboard_infos in list_storyboard_published:
        list_storyboard.append(storyboard_infos.id)

    for current_storyboard in list_storyboard:
        try:
            current_picture = storyboard_picture.objects.get(case_id=1, storyboard=current_storyboard)
            if current_picture.picture is None:
                list_profil_picture.append("bear.jpg")
            else:
                list_profil_picture.append(current_picture.picture)
        except:
            list_profil_picture.append("bear.jpg")

    infos = zip(list_storyboard_published, publish_user_infos, publish_like_infos, publish_fav_infos, list_profil_picture)

    return render(request, 'main/wall.html', locals())

@login_required
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

@login_required
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

@login_required
def getTextByID(request):
    list_text_id = []
    storyboard_id = request.POST.get("storyboard_id")
    text_id = request.POST.get("text_id")
    case_id = request.POST.get("case_id")
    response_data = {}

    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=storyboard_id, owner_id=request.user.id).order_by('case_id', 'text_order')
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_text_id.append(storyboard_text_infos_unit.id)

    text_id_final = list_text_id[int(text_id) - 1]
    get_text_with_id = storyboard_text.objects.get(id=text_id_final, storyboard_id=storyboard_id, case_id=case_id, owner_id=request.user.id)
    response_data['result'] = get_text_with_id.text

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
def updateListText(request):
    list_save_text = []
    list_all_text_final = []
    list_index = request.GET.get("list_num")
    id = request.GET.get("storyboard")
    storyboard_infos = storyboard.objects.get(id=id, owner_id=request.user.id)
    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=storyboard_infos.id).order_by('case_id', 'text_order')

    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)

    result_text_generation = storyboard_infos.last_text
    request.session['result_text_generation'] = result_text_generation
    list_generation_text = sent_tokenize(result_text_generation)
    list_all_text = list_save_text + list_generation_text

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

@login_required
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

    current_storyboard_picture = storyboard_picture.objects.get(storyboard=current_storyboard, case_id=case_id, owner_id=owner_id)
    current_storyboard_picture.picture = BytesIO(base64.b64decode(pictureB64)).read()
    current_storyboard_picture.save()

    return HttpResponse({"operation_result": "ok"})

@login_required
def generatePDF(request, id):
    list_save_text = []
    list_save_text_case = []
    list_save_picture = []
    list_picture_path = []
    default_blank_path = "tmp_pdf/blank.jpg"
    current_storyboard = storyboard.objects.get(id=id)

    fs = FileSystemStorage()
    path = fs.path("main/static/main/fonts/arial.ttf")

    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=current_storyboard.id)
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)
        list_save_text_case.append(storyboard_text_infos_unit.case_id)

    dict_text = dict()
    for case in range(1, 13):
        dict_text[case] = []
    for length in range(1, 13):
        for case, text in zip(list_save_text_case, list_save_text):
            if length == case:
                dict_text[case].append(text)


    storyboard_pictures_infos = storyboard_picture.objects.filter(storyboard_id=current_storyboard.id).order_by('case_id')
    for storyboard_pictures_infos_unit in storyboard_pictures_infos:
        list_save_picture.append(storyboard_pictures_infos_unit.picture)

    class PDF(FPDF):
        pass

    pdf = PDF(orientation='P', unit='mm', format='A4')

    for i in range(0, len(list_save_picture)):
        res = base64.b64encode(list_save_picture[i])
        im = Image.open(BytesIO(base64.b64decode(res)))
        im_size = im.size

        new_im = Image.new('RGB', (im_size[0], im_size[1] + 200), (255,255,255))
        new_im.paste(im, (0, 200))

        font = ImageFont.truetype(path, 22)
        draw = ImageDraw.Draw(new_im)
        current_text = " ".join(dict_text[i+1])
        lines = textwrap.wrap(current_text, width=50)
        y_text = 4

        for line in lines:
            width, height = font.getsize(line)
            draw.text((0, y_text), line, (0, 0, 0), font=font, align='center')
            y_text += height

        new_im.save("tmp_pdf/" + str(i+1) + ".jpg")

    image_number = len(list_save_picture)
    page_image_number = 6
    nb_page = (image_number // page_image_number)
    if image_number % page_image_number == 0:
        nb_page = (image_number // page_image_number) - 1

    for i in range(0, len(list_save_picture)):
        list_picture_path.append("tmp_pdf/" + str(i+1) + ".jpg")

    while nb_page >= 0:
        pdf.add_page()

        # left side
        pdf.rect(10, 20, 80, 80)
        pdf.rect(12, 22, 76, 76)

        pdf.rect(10, 115, 80, 80)
        pdf.rect(12, 117, 76, 76)

        pdf.rect(10, 210, 80, 80)
        pdf.rect(12, 212, 76, 76)

        # right side
        pdf.rect(120, 20, 80, 80)
        pdf.rect(122, 22, 76, 76)

        pdf.rect(120, 115, 80, 80)
        pdf.rect(122, 117, 76, 76)

        pdf.rect(120, 210, 80, 80)
        pdf.rect(122, 212, 76, 76)

        pdf.set_font('Arial', 'b', 15)
        pdf.cell(70, 1)
        pdf.cell(50, 5, current_storyboard.name + ' - Page ' + str(nb_page + 1), 0, 1, align='C')
        pdf.set_font('Arial', 'b', 10)

        for x in range(0, nb_page + 1):

            if x * 6 + 0 <= (len(list_picture_path) - 1):
                pdf.image(list_picture_path[x * 6 + 0], x=25, y=24, w=50, h=70, type='', link='')
            else:
                pdf.image(default_blank_path, x=25, y=24, w=50, h=70, type='', link='')

            if x * 6 + 1 <= (len(list_picture_path) - 1):
                pdf.image(list_picture_path[x * 6 + 1], x=135, y=24, w=50, h=70, type='', link='')
            else:
                pdf.image(default_blank_path, x=135, y=24, w=50, h=70, type='', link='')

            if x * 6 + 2 <= (len(list_picture_path) - 1):
                pdf.image(list_picture_path[x * 6 + 2], x=25, y=120, w=50, h=70, type='', link='')
            else:
                pdf.image(default_blank_path, x=25, y=120, w=50, h=70, type='', link='')

            if x * 6 + 3 <= (len(list_picture_path) - 1):
                pdf.image(list_picture_path[x * 6 + 3], 135, y=120, w=50, h=70, type='', link='')
            else:
                pdf.image(default_blank_path, 135, y=120, w=50, h=70, type='', link='')

            if x * 6 + 4 <= (len(list_picture_path) - 1):
                pdf.image(list_picture_path[x * 6 + 4], x=25, y=215, w=50, h=70, type='', link='')
            else:
                pdf.image(default_blank_path, x=25, y=215, w=50, h=70, type='', link='')

            if x * 6 + 5 <= (len(list_picture_path) - 1):
                pdf.image(list_picture_path[x * 6 + 5], x=135, y=215, w=50, h=70, type='', link='')
            else:
                pdf.image(default_blank_path, x=135, y=215, w=50, h=70, type='', link='')

        nb_page = nb_page - 1

    title_pdf = 'PDF-' + current_storyboard.name.replace(" ", "_") + '.pdf'
    pdf.output(title_pdf, 'F')

    path = 'tmp_pdf'
    files = os.listdir(path)
    for doc in files:
        if "blank" not in doc:
            os.remove(path + '/' + doc)

    filename = open(title_pdf, 'rb')
    content = filename.read()
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Length'] = os.path.getsize(title_pdf)
    response['Content-Disposition'] = 'attachment; filename=%s' % title_pdf
    filename.close()
    os.remove(title_pdf)

    return response

@login_required
def generateAbstract(request, id):
    list_save_text = []
    abstract_final = []
    current_storyboard = storyboard.objects.get(id=id)

    storyboard_text_infos = storyboard_text.objects.filter(storyboard_id=current_storyboard.id).order_by('case_id', 'text_order')
    for storyboard_text_infos_unit in storyboard_text_infos:
        list_save_text.append(storyboard_text_infos_unit.text)

    abstract = generate_abstract(list_save_text, 3)

    for current_save_text in list_save_text:
        for abstract_unit in abstract:
            if current_save_text == abstract_unit:
                abstract_final.append(abstract_unit)

    abstract_final = " ".join(abstract_final)

    current_storyboard.abstract = abstract_final
    current_storyboard.save()

    return redirect("/storyboard/" + str(id))