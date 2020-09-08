from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser 
from django.http import JsonResponse, HttpResponse
from .models import Object, Task_section, Task, Plan, Employee, Mens, Operation, Accept, Pass
import datetime 
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect
#from django.views.decorators.csrf import ensure_csrf_cookie
date_setting = datetime.date(2020, 6, 12)
@csrf_exempt   
def pass_operation(request,plan_id, operation_id):
        data = JSONParser().parse(request)
        count = data["count"]
        comment = data["comment"]
        plan = Plan.objects.get(id=plan_id)
        operation = Operation.objects.get(id=operation_id)
        p = Pass(operation=operation_id, plan=plan_id, count =count , salary=count*operation.price, comment= comment )
        p.save()
        return JsonResponse({"answer": "True"}, safe=False)
@csrf_exempt        
def take_task(request,plan_id):
        data = JSONParser().parse(request)
        plan = Plan.objects.get(id = plan_id)
        plan.take = data["is_take"]
        plan.comment = data["comment"]
        plan.save()
        return JsonResponse({"answer": "True"}, safe=False)


def operation_status(s, a, t1, t2, f):
    
    b = datetime.time(a.hour, a.minute, a.second)
    if b<t1:
        return 0 #не активна
    elif b<t2:
        return 1 #активна
    else:
        return 2 #просрочена

def get_operation(request,plan_id):
    result =[]    
    global date_setting
    a_t = datetime.datetime.now()
    plan = Plan.objects.get(id=plan_id)
    operations = Operation.objects.filter(plan = plan.id)
    status=[]
    for operation in operations:
        temp={}     
        temp["description"]=operation.description
        temp["place"]=json.loads(operation.place)
        mens = Mens.objects.get(id = operation.mens)
        temp["mens"]=mens.value
        temp["count"]= int(operation.count*100)/100
        temp["price"]=operation.price
        temp["salary"]=operation.salary
        temp["time_begin"]=operation.time1
        temp["time_finish"]= operation.time2
        passs = Pass.objects.filter(operation=operation.id, plan=plan.id)
        temp["is_pass"]=False
        temp["is_accept"]=False
        temp["pass_count"]=0.00
        temp["pass_salary"]=0.00
        temp["pass_comment"]=""
        temp["accept_count"]=0.00
        temp["accept_salary"]=0.00
        temp["accept_comment"]=""
        fact_salary=0
        for p in passs:
            temp["is_pass"]=True
            temp["pass_count"]=int(p.count*100)/100
            temp["pass_salary"]=p.salary
            fact_salary=p.salary
            temp["pass_comment"]=p.comment
        accept = Accept.objects.filter(operation=operation.id, plan=plan.id)
        for a in accept:
            temp["is_accept"]=True
            temp["accept_count"]=int(a.count*100)/100
            temp["accept_salary"]=a.salary
            fact_salary=a.salary
            temp["accept_comment"]=a.comment
        date1 = datetime.datetime(2020,9,9,operation.time1.hour, operation.time1.minute, operation.time1.second)
        date2 = datetime.datetime(2020,9,9,operation.time2.hour, operation.time2.minute, operation.time2.second)
        temp["cost_per_hour"]=int((operation.salary/((date2-date1).seconds//60)*60)*10)/10
        temp["cost_per_hour_fact"]=int(fact_salary/((date2-date1).seconds//60)*60*10)/10
        temp["status"]=operation_status(status, a_t, operation.time1, operation.time2,temp["is_pass"])
        status.append(temp["status"])
        now = datetime.datetime.now()
        if plan.date> datetime.date(now.year, now.month, now.day):
            status[-1]=0
            temp["status"]=0
        temp["operation_id"]=operation.id
        result.append(temp)
    return JsonResponse({"operations":result}, safe=False)
    
def get_task(request,employee_id):
    result={}
    #date = datetime.date.today()
    #if datetime.datetime.today().hour>=19:
    #    date+= datetime.timedelta(days=1)
    global date_setting
    date = date_setting
    plans = Plan.objects.filter(date=date, employee = employee_id)
    tasks=[]
    salary_predict=0
    salary_fact1=0
    salary_fact2=-1
    hours =0
    for plan in plans:
        if plan.take != False:
            temp={}
            task = Task.objects.get(id=plan.task)
            temp["plan_id"]=plan.id
   
            temp["task_name"]=task.descript
            task_section = Task_section.objects.get(id=task.task_section)
            temp["task_section"]=task_section.descript
            obj = Object.objects.get(id=task_section.object)
            temp["adress"]=obj.adres
            temp["is_take"]=str(plan.take)
            temp["task_id"]=plan.task
            hour1=task.time1.hour
            hour2=task.time2.hour
            temp["time_begin"]=str(task.time1)
            temp["time_end"]=str(task.time2)
            tasks.append(temp)
            hours+=hour2-hour1
            operations= Operation.objects.filter(plan=plan.id)
            for operation in operations:
                salary_predict+=operation.salary
                o_count=int(operation.count*100)
                pass_rows = Pass.objects.filter(operation = operation.id, plan = plan.id)
                for pass_row in pass_rows:
                    if int(pass_row.count*100)==o_count:
                        salary_fact1+=pass_row.salary
                accept_rows = Accept.objects.filter(operation = operation.id, plan = plan.id)
                for accept_row in accept_rows:
                    if salary_fact2==-1:
                        salary_fact2=0
                    #if int(accept_row.count*100)==o_count:
                    salary_fact2+=accept_row.salary
    result["tasks"]=tasks
    result["salary_predict"]=salary_predict
    if hours==0:
        result["cost_per_hour"]=0
    else:
        result["cost_per_hour"]=int(salary_predict/hours*10)/10
    result["is_accept"]=False
    result["salary_fact"]=0
    if salary_fact2>-1:
        result["is_accept"]=True
        result["salary_fact"]=salary_fact2
    if hours==0:
        result["cost_per_hour"]=0
        result["cost_per_hour_fact"]=0
    else:
        result["cost_per_hour"]=int(salary_predict/hours*10)/10
        result["cost_per_hour_fact"]=int(result["salary_fact"]/hours*10)/10
    return JsonResponse(result, safe=False)

def login(request,phone_number):
        employee = Employee.objects.get(phone_number = phone_number)
        id = employee.id
        f = employee.f
        i = employee.i
        o = employee.o
        return JsonResponse({"id": id, "f":f, "i":i, "o":o}, safe=False)


class Connect_accept(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            operation = Operation.objects.get(id = row["operation"])
            plan = Plan.objects.get(id = operation.plan)
            t, c = Accept.objects.update_or_create(id=row["number"],  defaults={"operation":row["operation"], "plan": plan.id, "count":row["count"], "salary":row["count"]*operation.price, "comment":row["coment"]})
        return JsonResponse({"answer": "True"}, safe=False)
class Connect_mens(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            t, c = Mens.objects.update_or_create(id=row["number"],  defaults={"value":row["value"] })
        return JsonResponse({"answer": "True"}, safe=False)
class Update(APIView): 
    def post(self,request):
        objects = Object.objects.all()
        self.dell(objects)
        objects = Task_section.objects.all()
        self.dell(objects)
        objects = Task.objects.all()
        self.dell(objects)
        objects = Plan.objects.all()
        self.dell(objects)
        objects = Employee.objects.all()
        self.dell(objects)
        objects = Mens.objects.all()
        self.dell(objects)
        objects = Operation.objects.all()
        self.dell(objects)
        objects = Accept.objects.all()
        self.dell(objects)
        objects= Pass.objects.all()
        self.dell(objects)
        return JsonResponse({"answer": "True"}, safe=False)
    def dell(self, data):
        for o in data:
            o.delete()

class Connect_operation(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            time1= datetime.time(row["hour1"], row["minute1"], 0)
            time2 = datetime.time(row["hour2"], row["minute2"], 0)
            task = Task.objects.get(id = row["task"])
            plan = Plan.objects.get(task = task.id, employee=row["employee"], date=task.date)
            t, c = Operation.objects.update_or_create(id = row["number"],defaults={ "time1":time1, "time2":time2, "place": row["place"], "description":row["descript"], "mens": row["mens"], "count":row["count"], "price":row["price"], "salary": row["count"]*row["price"], "plan":plan.id})
        return JsonResponse({"answer": "True"}, safe=False)
        
class Connect_pass(APIView): 
        
    def get(self,request):
        pass_rows = Pass.objects.all()
        answer = {}
        i=0
        for p in pass_rows:
            plan = Plan.objects.get(id=p.plan)
            temp={"id":p.id, "employee":plan.employee, "operation":p.operation, "count":p.count, "comment":p.comment}
            answer["row"+str(i)]=temp
            i+=1
        return JsonResponse(answer, safe=False)
        
class Connect_plan(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            date = datetime.date(row["year"],row["month"], row["day"])
            t, c = Plan.objects.get_or_create(date = date, task= row["task"], employee = row["employee"])
        return JsonResponse({"answer": "True"}, safe=False)
        
    def get(self,request):
        plan_rows = Plan.objects.all()
        answer = {}
        i=0
        for plan in plan_rows:
            if plan.take != None:
                temp={"id":plan.id, "task":plan.task, "employee":plan.employee, "take":plan.take, "comment":plan.comment}
                
                answer["row"+str(i)]=temp
                i+=1
        return JsonResponse(answer, safe=False)
            

class Connect_employee(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            t, c = Employee.objects.update_or_create(id = row["number"], defaults={"f":row["f"],"i":row["i"],"o":row["o"], "phone_number":row["phone_number"]})
        return JsonResponse({"answer": "True"}, safe=False)

class Connect_task(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            date = datetime.date(row["year"],row["month"], row["day"])
            time1= datetime.time(row["hour1"], row["minute1"], 0)
            time2 = datetime.time(row["hour2"], row["minute2"], 0)
            t, c = Task.objects.update_or_create(id = row["number"], defaults ={"date":date, "task_section":row["task_section"], "descript":row["descript"], "time1":time1, "time2":time2})
        return JsonResponse({"answer": "True"}, safe=False)

class Connect_task_section(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            t, c = Task_section.objects.update_or_create(id = row["number"], defaults = {"descript":row["name"], "object":row["object"]})
        return JsonResponse({"answer": "True"}, safe=False)

class Connect_object(APIView): 
    def post(self,request):
        data = JSONParser().parse(request)
        for row in data.values():
            t, c = Object.objects.update_or_create(id = row["number"], defaults={"adres":row["value"]})
        return JsonResponse({"answer": "True"}, safe=False)
            
    
    
class Connect(APIView): 
 
    def post(self,request):
        data = JSONParser().parse(request)
        l = data['row1']
        idd= l[0]
        date1 = datetime.date(l[1],l[2], l[3] )
        #time1 = datetime.time(l[4],l[5], l[6] )
        #time2 = datetime.time(l[7],l[8], l[9])
        #place =l[10]
        #description = l[11]
        #mens = l[12]
        #count = l[13]
        #price = float(l[14])
        #s1 = l[15].split(',')
        #employees = list(map(int, s1))
        #row, created = Task.objects.get_or_create(number = idd, date= date1, time1= time1, time2=time2, place =place, description=description, mens=mens, count=count, price=price)
        #row.save()
        #for emp in employees:
        #    t, c = Task_row.objects.get_or_create(date = date1, employee_number=emp, task_number = idd)
        #    t.save()
   
        #s1 = l[15].split(',')
        #employees = list(map(int, s1))
        

        #t, c = Task_row.objects.get_or_create(date = date1, employee_number=4, task_number = idd)
        #    t.save()

        #row = Exel_rows.objects.get(id=2)
        #row.value = exel['row2']
        #row.save()
        #row = Exel_rows.objects.get(id=3)
        #row.value = exel['row3']
        #row.save()
        return JsonResponse({"answer": "True"}, safe=False)
    def get(self,request):
        data = Get_row.objects.all()    
        serializer = Get_row_serializer(data, many=True) 
        return HttpResponse(serializer.data)
     








#from .models import Access_row, Exel_row, Get_row

#class Access_row_serializer(serializers.ModelSerializer):
#    class Meta:
#        model = Access_row
 #       fields = '__all__'
#class Exel_row_serializer(serializers.ModelSerializer):
#    class Meta:
#        model = Exel_row
#        fields = '__all__'
#class Get_row_serializer(serializers.ModelSerializer):
#    class Meta:
#        model = Get_row
#        fields = ('value',)
"""        
class Object_view(APIView):  
    def post(self,request):
        data1 = json.loads(request)
        for data in data1:
            values_for_update={"value":data["value"]}
            b, created = Object.objects.update_or_create(id=data["number"], defaults = values_for_update)

class Task_section_view(APIView):  
    def post(self,request):
        data1 = json.loads(request)
        for data in data1:
            values_for_update={"descript":data["name"], "object":data["object"]}
            b, created = Task_section.objects.update_or_create(id=data["number"], defaults = values_for_update)
        
class Task_view(APIView):  
    def post(self,request):
        data1 = json.loads(request)
        for data in data1:
            values_for_update={"descript":data["name"], "date":datetime.date(data["year"], data["month"],data["day"]), "task_section":data["task_section"], "time_begin":datetime.time(data["hour1"], data["minute1"]),"time_finish":datetime.time(data["hour2"], data["minute2"]), }
            b, created = Task.objects.update_or_create(id=data["number"], defaults = values_for_update)
class Employee_view(APIView):  
    def post(self,request):
        data = json.loads(request)
        values_for_update={"f":data["f"], "i":data["i"],"o":data["o"],"phone_number":data["phone_number"],}
        b, created = Employee.objects.update_or_create(id=data["number"], defaults = values_for_update)


class Plan_view(APIView):  
    def post(self,request):
        data1 = json.loads(request)
        for data in data1:
            values_for_update={"date":datetime.date(data["year"], data["month"],data["day"]), "task":data["task"],  "employee":data["employee"]}
            b, created = Plan.objects.update_or_create(id=data["number"], defaults = values_for_update)
    def get(self,request): 
        plans = Plan.objects.all()
        result={}
  #      for i,plan in enumerate(plans):
   #         if plan["is_take"]!= None: 
    #            result[i]={"id":plan.id, "task":plan.task, "employee":plan.employee, "take":plan.is_take, "comment":plan.comment}
        return JsonResponse(result, safe=False)
        
class Operation_view(APIView):  
    def post(self,request):
        data1 = json.loads(request)
        for data in data1:
            plan = Plan.objects.get(task=data["task"], employee=data["employee"])
            time1 = datetime.time(data["hour1"], data["minute1"])
            time2 = datetime.time(data["hour2"], data["minute2"])
            values_for_update={"time_begin":time1, "time_finish":time2, "descript":data["descript", "adress":data[""], "mensure":data["mens"],"count":data["count"], "price":data["price"], "plan":plan.id }
            b, created = Operation.objects.update_or_create(id=data["number"], defaults = values_for_update)        
     
class Accept_view(APIView):  
    def post(self,request):
        data1 = json.loads(request)
        for data in data1:
            values_for_update={"operation":data["operation"], "count":data["count"],"comment":data["coment"]}
            b, created = Accept.objects.update_or_create(id=data["number"], defaults = values_for_update)       
        
class Pass_view(APIView):
    def get(self,request): 
        ps = Pass.objects.all()
        result={}
 #       for i,p in enumerate(ps):
 #           result[i]={"id":p.id, "operation":p.operation, "employee":plan.employee, "count":plan.count, "comment":plan.comment}
        return JsonResponse(result, safe=False)        
        
        """
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        