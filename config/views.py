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


class QuizView(TemplateView):
    """Quiz page for students."""

    template_name = 'pages/survey.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        try:
            userprof = UserProfile.objects.get(user=request.user)
        except:
            return HttpResponseRedirect('/')
        mentors = Mentors.objects.filter(girl=userprof)
        if len(userprof.qna) > 0 and userprof.signup_type == 2:
            return HttpResponseRedirect('/profile/match/')
        elif len(mentors) > 0 and userprof.signup_type == 1:
            return HttpResponseRedirect('/profile/match/')
        else:
            questions = load_questions("questions_final.csv")
            return render(request, self.template_name, {'questions': questions})


class ResultView(TemplateView):
    """Home page for students."""

    template_name = 'pages/profile.html'

    def post(self, request, *args, **kwargs):
        """Method for get request of home page."""
        name = request.POST['name']
        # description = request.POST['description']
        questions = load_questions("questions_final.csv")
        answer = []
        for i in range(0, len(questions)):
            try:
                ans = request.POST['options_' + str(i + 1)]
            except:
                ans = ''
            answer.append(ans)

        userprof = UserProfile.objects.filter(user=request.user)
        if userprof[0].signup_type == 2:
            userprof.qna = answer
            userprof.save()

        if name == 'Your name' or name == '':
            name = ''
        else:
            name = " " + name

        mentor_answers = load_mentor_answers("mentor_answers.csv")
        match = get_mentor_match(answer, mentor_answers)

        # q1 = request.args.getlist('Q1').decode('utf-8')
        # write_log_file(SURVEY_RESULTS, json.dumps(q1) + "\tMATCHED TO: %s" % match)

        links = load_mentor_names("mentor_links_final.csv")
        profiles, mentor_questions = load_mentor_profiles(
            "mentor_profilesfinalv2.csv",
            "mentor_profilesfinalv3.csv",
            csv_file=True
        )
        return render(
            request,
            self.template_name,
            {
                'message1': "Congratulations%s!" % name,
                'message2': "Your mentor is: ",
                'name': links[match],
                'key': match,
                'mentor_questions': mentor_questions,
                'profile': profiles[match]
            }
        )
        return render(request, self.template_name, {})


class ProfileView(TemplateView):
    """Home page for students."""

    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        return render(request, self.template_name, {})
