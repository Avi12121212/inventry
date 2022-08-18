import json
import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect


def index(request):
    result = "not found"
    value1 = ""
    naam = ""
    count = 0
    d = {"rohit": "programming in c",
         "shubham": "80%",
         "shyam": "78%",
         "harsh": "80%",
         "Aman ": "85%",
         "suraj": "work on java",
         }
    if request.GET:
        naam = request.GET["name"]
        for name, value in d.items():
            if naam == name or naam == value:
                result = name
                value1 = value
    return render(request, "a.html", {"d": d, "result": result, "value": value1, "name": naam})


def login(request):
    title = ""
    session = request.session
    try:

        del session["answers"]
    except:
        pass
    if request.POST:
        # email = request.POST['email']
        # password = request.POST['password']
        title = request.POST['title']
        session["name"] = title
        return redirect("/quiz/")
        # return render(request, "quiz.html", {"title": title, "session": session})
    return render(request, "login.html", {"session": session})


# <<<---- Login Page Ends Here ---->>

def quiz(request):
    answers = request.session.get("answers")
    if answers == None:
        answers = []

    q1 = {"question": "What is C?", "op1": "Language", "op2": "Alphabet", "op3": "Ascii character",
          "op4": "All of these", "correct": "a"}
    q2 = {"question": "Who developed Python Programming language?", "op1": "Wick van rossum", "op2": "Dennis Ritchie",
          "op3": "Guido van Rossum", "op4": "none", "correct": "c"}
    q3 = {"question": "Which of the following is the correct extension of the python file?", "op1": ".python",
          "op2": ".pl", "op3": ".py", "op4": ".p", "correct": "c"}
    q4 = {"question": "Who developed C programming language ?", "op1": "denies ritchies", "op2": "Guido van Rossum",
          "op3": "harsh", "op4": "none", "correct": "a"}
    q5 = {"question": "Django is  a ?", "op1": "Programming Language", "op2": "Framework",
          "op3": "Python Web Framework", "op4": "None", "correct": "c"}
    questions = [q1, q2, q3, q4, q5]
    questionno = 0
    givenanswer = ""
    correctanswer = ""
    result = ""
    totalmarks = 0
    if not request.POST:
        try:
            del request.session["answers"]
        except:
            pass
    if request.POST:
        givenanswer = request.POST["option"]
        questionno = int(request.POST["qno"])
        totalmarks = int(request.POST["totalmarks"])
        correctanswer = questions[questionno].get("correct")
        questionno += 1
        totalmarks += 1
        result = "Yes"

        if givenanswer != correctanswer:
            result = "No"
            totalmarks -= 1
        data = {"qno": (questionno - 1), "answer": givenanswer, "correct": correctanswer, "result": result}
        answers.append(data)
        if questionno >= len(questions):
            return render(request, 'result.html', {"totalmarks": totalmarks,
                                                   "answers": answers})
    # return httpResponse('python quiz!')
    request.session["answers"] = answers
    return render(request, "quiz.html",
                  {"question": questions[questionno],
                   "showqno": questionno + 1,
                   "qno": questionno,
                   "givenanswer": givenanswer,
                   "correctanswer": correctanswer,
                   "result": result,
                   "totalmarks": totalmarks, "answers": answers})


def birthday(request):
    birth = ""
    name = ""
    names = {"Avinash": "28/8/95",
             "shyam": "8/7/00",
             "Rohit": "15/8/00",
             "sachin": "19/1/02",
             "harsh": "29/2/00",
             "shivam": "7/4/00",
             "Abhishek": "13/9/91",
             "sagar": "27/7/00",
             "ashutosh": "12/3/00",
             "saktiman": "12/7/01"
             }
    try:
        name = request.GET["name"]
        name.lower()
        birth = names.get(name)

        if birth == None:
            output = {"status": "error", "country": "india", "name": "notfornd".lower(), "DOB": "noDATE".upper()}
            return HttpResponse(json.dumps(output))

        else:
            output = {"status": "ok", "country": "india", "name": name.lower(), "DOB": birth.upper()}
            return HttpResponse(json.dumps(output))
    except:
        output = {"status": "ok", "country": "india", "name": name.lower(), "DOB": birth.upper()}
        return HttpResponse(json.dumps(output))


def pythonquiz(request):

    q1 = {"question": "What is C?", "op1": "Language", "op2": "Alphabet", "op3": "Ascii character",
          "op4": "All of these", "correct": "a"}
    q2 = {"question": "Who developed Python Programming language?", "op1": "Wick van rossum", "op2": "Dennis Ritchie",
          "op3": "Guido van Rossum", "op4": "none", "correct": "c"}
    q3 = {"question": "Which of the following is the correct extension of the python file?", "op1": ".python",
          "op2": ".pl", "op3": ".py", "op4": ".p", "correct": "c"}
    q4 = {"question": "Who developed C programming language ?", "op1": "denies ritchies", "op2": "Guido van Rossum",
          "op3": "harsh", "op4": "none", "correct": "a"}
    q5 = {"question": "Django is  a ?", "op1": "Programming Language", "op2": "Framework",
          "op3": "Python Web Framework", "op4": "None", "correct": "c"}
    questions = [q1, q2, q3, q4, q5]

    return HttpResponse(json.dumps(questions), content_type='application/json')


def bookssearch(request):
    searchValue = ""
    b={}
    if request.GET:
        searchValue = request.GET["searchValue"]

        path = "https://www.googleapis.com/books/v1/volumes?q={0}".format(searchValue)
        # print(path)
        url = requests.get(path)
        # print(response.json())
        books = json.loads(url.text)
        print(len(books), type(books))
        # for book in books:
        #     print(book)
        # b = json.dumps(books)
        b = books["items"]
        print(b)
    return render(request, "bookslist.html", {"books": b,"searchValue":searchValue})
    # return HttpResponse(json.dumps(books), content_type='application/json')
