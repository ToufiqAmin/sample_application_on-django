from django.shortcuts import render

from django.http import HttpResponse
from .models import seismicdataforexam
from django.core.paginator import Paginator
import re


rowNumber = None
searchItems = None


def home(request):

    # pageNumber = str(request.GET.get('page'))
    global rowNumber
    rowNumber = request.GET.get('row_number')
    if rowNumber == None:
        rowNumber = 10

    # data = {
    #     'row': rowNumber,
    #     'page': pageNumber
    # }

    return render(request, "index.html")

def search(request):
    global searchItems
    data = None
    testItems = request.GET.get('searchItems')
    searchParam = None
    searchParamList = None
    print("searchItems: ", searchItems)
    print("testItems: ", testItems)

    if testItems != None and searchItems == None:
        searchItems = testItems
    elif testItems != None and searchItems != None:
        searchItems = testItems

    print("searchItems: ", searchItems)
    print("testItems: ", testItems)  

    if searchItems == None:
        data = seismicdataforexam.objects.all().values()
    else:

        searchItems_length = len(searchItems)
        print("searchItems: ", searchItems)
        print("Length of searchItems: ", searchItems_length)
        # startPoint = searchItems.find(r'“')
        # endPoint = searchItems.find(r'”')
        startPoint = searchItems.find(r'"')
        endPoint = searchItems.rfind(r'"')
        searchLiteral = searchItems[startPoint+1:endPoint]
        print("startPoint: ", startPoint)
        print("endPoint: ", endPoint)
        print("SearchLiteral: ", searchLiteral)
        #if "%d" is not in 0 postion of input
        if startPoint != 0:
            #if - is not the 0 position of input
            if searchItems[0] != '-':
                x = re.search("^PM...", searchLiteral)
                if x:
                    print("Stage 1 passed")
                    if searchItems[startPoint-1] == ' ':
                        searchParam = searchItems[0:startPoint-1]
                        # data = seismicdataforexam.objects.filter(region__startswith=search_param, block=searchLiteral).values()
                        data = seismicdataforexam.objects.filter(block=searchLiteral).values() | seismicdataforexam.objects.filter(region__startswith=searchParam).values()
                    elif searchItems[startPoint-1] == '-':
                        searchParam = searchItems[0:startPoint-1]
                        data = seismicdataforexam.objects.filter(region__startswith=searchParam).exclude(block=searchLiteral).values()
                else:
                    print("Stage 2 passed")
                    if searchItems[startPoint-1] == ' ':
                        searchParam = searchItems[0:startPoint-1]
                        searchParamList = searchParam.split(' ')
                    index = searchLiteral.find('.')
                    searchParamListLength = len(searchParamList)
                    if index != -1:
                        i = searchLiteral[0:index]
                        j = searchLiteral[index+2:]
                        # if searchParamListLength == 1:
                        #     data = seismicdataforexam.objects.filter(length_km__range=(i, j)).values() | seismicdataforexam.objects.filter(block=searchParam).values()
                        # elif searchParamListLength == 2:
                        #     data = seismicdataforexam.objects.filter(length_km__range=(i, j)).values() | seismicdataforexam.objects.filter(block=searchParamList[0]).values() | seismicdataforexam.objects.filter(block=searchParamList[1]).values()
                        for x in range(searchParamListLength):
                            if data == None:
                                data = seismicdataforexam.objects.filter(length_km__range=(i, j)).values() | seismicdataforexam.objects.filter(block=searchParamList[x]).values()
                            else:
                                data2 = seismicdataforexam.objects.filter(length_km__range=(i, j)).values() | seismicdataforexam.objects.filter(block=searchParamList[x]).values()
                                data = data | data2
            # if - is zero position of input
            else:
                data = seismicdataforexam.objects.all().exclude(block=searchLiteral).values()
        # if "%d" is zero position of input
        else:
            print("Stage 3 passed")
            x = re.search("^PM...", searchLiteral)
            if x:
                #spliting input in two 
                searchLiteral = searchLiteral.split(' ')
                searchLiteralLength=len(searchLiteral)
                #using for loop to search * and merge dictionaries
                for x in range(searchLiteralLength):
                    word = searchLiteral[x]
                    print("Word: ", word)
                    for j in range(len(word)):
                        #if * is in last postions of word
                        if word[j] == '*' and j > (len(word)//2):
                            print("stage 4 passed")
                            word = word[0:j]
                            if data == None:
                                print("stage 4 if con. passed")
                                data = seismicdataforexam.objects.filter(block__startswith=word).values()
                            else:
                                data2 = seismicdataforexam.objects.filter(block__startswith=word).values()
                                data = data | data2
                        #if * is in first position of word
                        elif word[j] == '*' and j==0:
                            print("stage 4 else if con. 1 passed")
                            word = word[j+1: ]
                            if data == None:
                                data = seismicdataforexam.objects.filter(block__endswith=word).values()
                            else:
                                data2 = seismicdataforexam.objects.filter(block__endswith=word).values()
                                data = data | data2
                            break
                        #if there is no * in the word
                        elif j == len(word)-1 and word[j] != '*':
                            print("stage 4 else con. 1 passed")
                            if data == None:
                                data = seismicdataforexam.objects.filter(block=word).values()
                            else:
                                data2 = seismicdataforexam.objects.filter(block=word).values()
                                data = data | data2        
            else:
                # "%d..%d" is only input
                index = searchLiteral.find('.')
                # searchParamListLength = len(searchParamList)
                if index != -1:
                    i = searchLiteral[0:index]
                    j = searchLiteral[index+2:]
                    data = seismicdataforexam.objects.filter(length_km__range=(i, j)).values()

    
    # data.update(mew_data)
    
    # paginator Manual
    # rowNumber = request.GET.get('row_number')
    # print("rowNumber: ", rowNumber)
    paginator = Paginator(data, rowNumber)
    pageNumber = request.GET.get('page')
    # if Number of Page is None
    # if pageNumber == None:
    #     pageNumber = 10
    dataFinal = paginator.get_page(pageNumber)

    # try:
    #     dataFinal = paginator.get_page(pageNumber)
    # except PageNotAnInteger:
    #     dataFinal = paginator.page(1)
    # except EmptyPage:
    #     dataFinal = paginator.page(1)

    # formData = {"searchItems": searchItems}


    return render(request, "index.html", context = {'myData': dataFinal})


def configurationPage(request):
    print("Configuration Page")
    return render(request, "configuration_page.html")