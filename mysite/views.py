import base64

import speech_recognition as sr
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Keyword, Algorithm


class QueryView(View):

    def post(self, request):
        try:
            words = request.POST.get("input_text").split()
            score = {}
            best_match = None
            for word in words:
                keyword = Keyword.objects.all().filter(word=word)
                print(keyword)
                if len(keyword) == 1:
                    keyword = keyword[0]
                    for algorithm in keyword.algorithm_set.all():
                        if algorithm.name in score:
                            score[algorithm.name] += keyword.weight
                        else:
                            score[algorithm.name] = keyword.weight

                        if not best_match or score[algorithm.name] > score[best_match]:
                            best_match = algorithm.name
            print(best_match)
            return JsonResponse(
                {
                    "success": True,
                    "text": Algorithm.objects.get(name=best_match).implementation
                }
            )

        except Exception as e:

            return JsonResponse(
                {
                    "success": False,
                    "message": "An error occurred: " + str(e),
                    "words": '"' + request.POST.get("input_text") + '"'
                }
            )

    def get(self, request):
        return render(request, 'index.html')


# def Speech_recognition(audio):
#     r = sr.Recognizer()
#     # with sr.Microphone() as source:
#     #     print("Höre zu...")
#     #     audio = r.listen(source)
#     try:
#         x = r.recognize_google(sr.AudioData(audio))
#         # x = r.recognize_google(audio, language = "de_DE")
#         print("recognised text: " + str(x))
#     except sr.UnknownValueError:
#         print("Could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
#     return (x)
#
