from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from keshe.models import *
import json


# Create your views here.
# 是否登录
def is_login(request):
    if "is_login" in request.session:
        return True
    else:
        return False


# 全部图书
def all_books(request):
    res = {"book_data": [
        {"b_id": i.b_id, "b_name": i.b_name, "b_author": i.b_author, "b_isbn": i.b_isbn, "b_public": i.b_public,
         "b_total": i.b_total,
         "b_lave": i.b_lave, "is_borrowable": i.b_total - i.b_lave > 0} for i in
        Book.objects.all()]}
    print(res)
    return JsonResponse(res)


# 图书分类
def book_type(request):
    res = {"b_type": [i.bookType for i in BookType.objects.all()]}
    print(res)
    return JsonResponse(res)


# 借阅图书
def borrow(request):
    book_id = json.loads(request.body)["book_id"]
    book = Book.objects.get(b_id=book_id)
    d = {"code": 200}
    if book.b_total - book.b_lave > 0:
        try:
            if request.session["picked"] == 1:
                person = Teacher.objects.get(username=request.session["user_name"])
                if person.type.max_borrow - person.borrow > 0:
                    book.b_lave += 1
                    book.save()
                    person.borrow += 1
                    person.save()
                    borrow = BorrowTeacher(teacher=person, book=book)
                    borrow.save()
                    d["code"] = 100

            else:
                person = Student.objects.get(username=request.session["user_name"])
                if person.max_borrow - person.borrow > 0:
                    book.b_lave += 1
                    book.save()
                    person.borrow += 1
                    person.save()
                    borrow = BorrowStudent(student=person, book=book)
                    borrow.save()
                    d["code"] = 100
        except:
            d["code"] = 200
    return JsonResponse(d)


def index(request):
    return render(request, "index.html")


def page0(request):
    return render(request, "page0.html")


def page1(request):
    if not is_login(request):
        return redirect("/page4")
    return render(request, "page1.html")


def page2(request):
    if not is_login(request):
        return redirect("/page4")
    return render(request, "page2.html")


def page3(request):
    if not is_login(request):
        return redirect("/page4")
    return render(request, "page3.html")


def page4(request):
    if is_login(request):
        return redirect("/page3")
    return render(request, "page4.html")


def page5(request):
    if is_login(request):
        return redirect("/page3")
    return render(request, "page5.html")


# 注册
def sign_up(request):
    res = json.loads(request.body)
    d = {"code": 200}
    try:
        if res["picked"] == "学生":
            person = Student.objects.create_user(username=res["us_name"], password=res["password_1"],
                                                 email=res["email"])
            d["code"] = 100
        else:
            person = Teacher.objects.create_user(username=res["us_name"], password=res["password_1"],
                                                 email=res["email"],
                                                 type=Type.objects.get(id=res["job_title"]))
            d["code"] = 100
    except:
        d["code"] = 200
    return JsonResponse(d)


# 登录
def login(request):
    d = {"code":200}
    res = json.loads(request.body)
    print(res)
    person = authenticate(request, username=res["user_name"], password=res["password"])
    if person:
        request.session.set_expiry(60 * 60 * 24 * 7)
        request.session["user_name"] = res["user_name"]
        request.session["is_login"] = True
        if len(Teacher.objects.filter(username=res["user_name"])) == 1:
            request.session["picked"] = 1
        else:
            request.session["picked"] = 0
        d["code"] = 100
    else:
        d["code"] = 200
    print(d)
    return JsonResponse(d)


# 用户信息
def user_inf(request):
    d = {}
    if request.session["picked"] == 0:
        person = Student.objects.get(username=request.session["user_name"])
        d["user_inf"] = {"user_name": person.username, "user_title": "学生", "user_total": person.max_borrow,
                         "user_borrow": person.borrow}
    else:
        person = Teacher.objects.get(username=request.session["user_name"])
        d["user_inf"] = {"user_name": person.username, "user_title": person.type.type,
                         "user_total": person.type.max_borrow,
                         "user_borrow": person.borrow}
    print(d)
    return JsonResponse(d)


# 已借阅
def borrowed_arr(request):
    res = {}
    person = None
    books = None
    if request.session["picked"] == 0:
        person = Student.objects.get(username=request.session["user_name"])
        books = BorrowStudent.objects.filter(student=person)
    else:
        person = Teacher.objects.get(username=request.session["user_name"])
        books = BorrowTeacher.objects.filter(teacher=person)
    res["borrowed_arr"] = [{"book_id": i.book.b_id, "book_name": i.book.b_name, "book_author": i.book.b_author,
                            "book_borrow": i.borrow_date,
                            "book_return": i.borrow_date + timezone.timedelta(days=30),
                            "is_expected": timezone.now().date() > (i.borrow_date + timezone.timedelta(days=30))} for i
                           in books]
    print(res)
    return JsonResponse(res)


# 还书
def return_book(request):
    res = {"code": 200}
    person = None
    books = None
    book = json.loads(request.body)
    print(book["book_id"])
    print(request.session["picked"])
    if "book_id" in book:
        try:
            if request.session["picked"] == 0:
                person = Student.objects.get(username=request.session["user_name"])
                books = BorrowStudent.objects.filter(student=person, book=Book.objects.get(b_id=int(book["book_id"])))
                person.borrow -= 1
                bk = books[0].book
                bk.b_lave -= 1

            else:
                person = Teacher.objects.get(username=request.session["user_name"])
                books = BorrowTeacher.objects.filter(teacher=person, book=Book.objects.get(b_id=int(book["book_id"])))
                person.borrow -= 1
                bk = books[0].book
                bk.b_lave -= 1
        except:
            res["code"] = 200
        else:
            person.save()
            bk.save()
            books[0].delete()
            res["code"] = 100
    return JsonResponse(res)


# 图书分类
def classification(request):
    bookTypes = BookType.objects.all()
    res = {"b_type": [i.bookType for i in bookTypes]}
    print(res)
    return JsonResponse(res)


# 分类书信息
def get_class_value(request):
    res = {}
    indexs = json.loads(request.body)
    if "classification" in indexs:
        print(indexs["classification"])
        books = Book.objects.filter(b_type=BookType.objects.get(id=int(indexs["classification"])))
        print(books)
        res["books"] = [
            {"b_id": i.b_id, "b_name": i.b_name, "b_author": i.b_author, "b_isbn": i.b_isbn, "b_public": i.b_public,
             "b_total": i.b_total,
             "b_lave": i.b_lave, "is_borrowable": i.b_total - i.b_lave > 0} for i in books]
    print(res)
    return JsonResponse(res)


# 搜索
def search(request):
    if "keyword" in request.GET:
        books = Book.objects.filter(b_name__contains=request.GET["keyword"])
        res = {"book_data_select": [
            {"b_id": i.b_id, "b_name": i.b_name, "b_author": i.b_author, "b_isbn": i.b_isbn, "b_public": i.b_public,
             "b_total": i.b_total,
             "b_lave": i.b_lave, "is_borrowable": i.b_total - i.b_lave > 0} for i in books
        ]}
        print(res)
    return JsonResponse(res)


def logout(request):
    request.session.clear()
    return redirect("/page4")
