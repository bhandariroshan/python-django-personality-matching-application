"""View for dashboard."""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .survey import load_mentor_names
from .survey import load_mentor_answers
from .survey import load_questions, load_mentor_profiles, get_mentor_match
from sciencerunaway.users.models import UserProfile, Mentors
# import json
from django.template.defaulttags import register


MAILING_LIST = "mailing_list.txt"
SURVEY_RESULTS = "survey_results.txt"


def match_mentor(user):
    all_role_models = UserProfile.objects.filter(signup_type=2)
    current_user = UserProfile.objects.filter(user=user)

    current_user_answer = current_user[0].common_answers
    current_user_answer = [x.lower() for x in current_user_answer]

    match = None
    best_score = 0

    for each_user in all_role_models:
        current_best = 0
        mentor_answers = each_user.common_answers

        ment_ans = [x.lower() for x in mentor_answers]

        for (a, b) in zip(current_user_answer, ment_ans):
            if a == b:
                current_best += 1

        if current_best > best_score:
            best_score = current_best
            match = each_user
    Mentors.objects.create(
        girl=current_user[0],
        mentor=match
    )

    return match


@register.filter
def get_question(count):
    profiles, mentor_questions = load_mentor_profiles(
        "mentor_profilesfinalv2.csv",
        "mentor_profilesfinalv3.csv",
        csv_file=True
    )
    try:
        return mentor_questions[count]
    except:
        return ''


class HomeView(TemplateView):
    """Home page for students."""

    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        return render(request, self.template_name, {})


class AboutView(TemplateView):
    """Home page for students."""

    template_name = 'pages/about.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        return render(request, self.template_name, {})


class ContactView(TemplateView):
    """Home page for students."""

    template_name = 'pages/contact.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        return render(request, self.template_name, {})


class MailView(TemplateView):
    """Home page for students."""

    template_name = 'pages/thanks.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        # q1 = request.args
        # email = q1['comments']
        # if email!='':
        # write_log_file(MAILING_LIST, email)
        # return render_template('thanks.html')
        return render(request, self.template_name, {})


class GalleryView(TemplateView):
    """Home page for students."""

    template_name = 'pages/gallery.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        # mk = links.keys()
        # random.shuffle(mk)
        # return render_template('gallery.html', images = mk[:16], profiles = profiles)
        return render(request, self.template_name, {})


class ProfileActivationView(TemplateView):
    """Home page for students."""

    template_name = 'pages/activate.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        # mk = links.keys()
        # random.shuffle(mk)
        # return render_template('gallery.html', images = mk[:16], profiles = profiles)
        return render(request, self.template_name, {})


class QuizView(TemplateView):
    """Quiz page for students."""

    template_girls = 'pages/survey_girls.html'
    template_models = 'pages/survey_models.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        try:
            userprof = UserProfile.objects.get(user=request.user)
        except:
            username = request.session.get('username', '')
            if username:
                userprof = UserProfile.objects.get(user__username=username)
            else:
                return HttpResponseRedirect('/')

        # mentors = Mentors.objects.filter(girl=userprof)
        common_len = 0
        if userprof.common_answers:
            common_len = len(userprof.common_answers)

        if common_len > 0 and userprof.signup_type == 2:
            return HttpResponseRedirect('/profile/match/')
        elif common_len > 0 and userprof.signup_type == 1:
            return HttpResponseRedirect('/profile/match/')
        else:
            if userprof.signup_type == 1:
                # questions = load_questions("questions_final.csv")
                return render(request, self.template_girls, {})
            else:
                return render(request, self.template_models, {})


class ResultView(TemplateView):
    """Home page for students."""

    template_name = 'pages/profile.html'

    def post(self, request, *args, **kwargs):
        """Method for get request of home page."""
        try:
            userprof = UserProfile.objects.filter(user=request.user)
        except:
            username = request.session.get('username', '')
            if username:
                userprof = [UserProfile.objects.get(user__username=username)]

        myprofile = userprof[0]

        common_questions_length = 5
        role_models_questions_length = 14

        name = request.POST.get('name', '')
        linkedin = request.POST.get('linkedin', '')
        bio = request.POST.get('bio', '')

        common_answer = []
        role_answer = []

        for i in range(0, common_questions_length):
            ans = request.POST.get('common' + str(i + 1), '')
            common_answer.append(ans)

        if myprofile.signup_type == 2:
            for i in range(0, role_models_questions_length):
                ans = request.POST.get('question' + str(i + 1))
                role_answer.append(ans)

        if name != '':
            myprofile.name = name

        myprofile.common_answers = common_answer
        myprofile.other_answers = role_answer

        if linkedin != '':
            myprofile.linkedin = linkedin

        myprofile.bio = bio
        myprofile.save()

        if myprofile.user.is_active:
            return HttpResponseRedirect('/profile/match/')
        else:
            return HttpResponseRedirect('/profile/activation/')


class ProfileView(TemplateView):
    """Home page for students."""

    template_name = 'pages/profile.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        userprof = UserProfile.objects.get(user=request.user)
        if userprof.signup_type == 1:
            mentors = Mentors.objects.filter(girl=userprof)
            if len(mentors) == 0:
                mentor = match_mentor(request.user)
            else:
                mentor = mentors[0]
        else:
            girls = Mentors.objects.filter(mentor=userprof)

        if userprof.signup_type == 1:
            return render(
                request,
                self.template_name,
                {
                    'mentor': mentor,
                    'userprof': userprof
                }
            )
        else:
            return render(
                request,
                self.template_name,
                {
                    'girls': girls,
                    'userprof': userprof
                }
            )
