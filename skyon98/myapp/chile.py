import operator
import random

operators = [('+', operator.add), ('-', operator.sub), ('*', operator.mul)]


a, b = input().split()
a = int(a)
b = int(b)
op, fn = random.choice(operators)
#print("{} {} {} = {}".format(a, op, b, fn(a, b)))
print("the value of op is:", op)
print("the value of fn is:", fn)
print(type(fn))



if(request.method == 'POST'):
        userotp = request.POST.get("taccno")
        if (userotp == calculatedotp):
            messages.success(
                request, "Your Money Has Been Transfered Successfully .")
            return HttpResponse("Successfull")
        else:
            messages.error(
                request, "Your Money Has NOT Been  Transfered. Please try again. Sorry for inconvience caused")
    

