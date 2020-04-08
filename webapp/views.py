import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render , render_to_response , get_object_or_404 , redirect

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view

from webapp.models import Case
from webapp.serializers import CaseSerializers


sumModules = {
    "arch": ["Summit - System level" , "Summit - DB Architecture/Interfaces" ,
              "Summit - User Interface / FT Framework" , "Summit - DB Admin / Upgrade" ,
              "Summit - Extendibility / Meta Data" , "Summit - RT Server Architecture And Admin" ,
              "Summit - Reporting Framework" , "Summit - Performance" ,
              "Summit - User Documentation" , "Summit - Utilities/Static Data" ] ,
    "fo" : ["Summit - Toolkit/Pricing Models" , "Summit - OTC Derivatives" , "Summit - Equities" ,
            "Summit - Fixed Income" , "Summit - Bond Issuance" , "Summit - Cash Management/Settlement Processing" ,
            "Summit - RTF/MKTDATA" , "Summit - Toolkit/Pricing Models", "Summit - Treasury" , "Summit - Fixed Income","Summit - Structured Products/MUST" , "Summit - Equity/Equity Derivatives"  ] ,
    "risk" : ["Summit - Market Risk Limits" , "Summit - Credit risk" , "Summit - Historical VAR" , "Summit - CCP" ,
              "Summit - GAP Analysis / Cash Analysis" , "Summit - APAC - Credit Limit" ,
              "Summit - Risk Management / RT Risk", "Summit - Credit Derivatives"] ,
    "bo" : ["Summit - Buyside" , "Summit - GBO" ,
            "Summit - Operations" , "Summit - Commercial Lending" ,
            "Summit - Collateral Management" , "Summit - Security Finance" ,
            "Summit - Post Trade Booking Processing" , "Summit - Back Office Positioning" ,
            "Summit - Back Office Documentation Engine" ,
            "Summit - Operations/Documentation" , "Summit - Security / STD"] ,
    "acct" : ["Summit - Accounting", "Summit - P&L", "Summit - Hedge Accounting/FAS133"]
}

@api_view(["GET"])
def getAllCases(request):
    try:
        cases = Case.objects.all()
        serializer = CaseSerializers(cases, many=True)
        return JsonResponse({'cases' : serializer.data}, safe = False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse ( {'error' : str ( e )} , safe = False , status = status.HTTP_404_NOT_FOUND )
    except Exception :
        return JsonResponse ( {'error' : "Something went wrong"} , safe = False ,
                              status = status.HTTP_500_INTERNAL_SERVER_ERROR )

@api_view(["GET"])
def cases(request):
    try:
        cases = Case.objects.filter(published=0)
        serializer = CaseSerializers(cases, many=True)
        return JsonResponse({'cases' : serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR

                            )

@api_view(["GET"])
def viewCase(request, caseID):
    try:
        case = Case.objects.get(caseID=caseID)
        serializer = CaseSerializers(case)
        return JsonResponse({'case': serializer.data}, safe = False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe = False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': "Something went wrong"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_cases(request):
    case = Case()
    case.caseID = '2'
    case.caseNumber = 'Test 2'
    case.caseSubject = 'Desc 2'
    case.caseDescription = 'fo'
    case.caseModule = 'Summit - Fo '
    case.published = 0

    case.save()

    case = Case ( )
    case.caseID = '3'
    case.caseNumber = 'Test 3'
    case.caseSubject = 'Desc 3'
    case.caseDescription = 'fo'
    case.caseModule = 'Summit - Fo '
    case.published = 0

    case.save ( )


def allcases(request):
    resp = getAllCases(request)
    resp = json.loads(resp.content.decode('utf-8'))
    context = {}
    context["cases"] = resp['cases']
    context["modules_acct"] = sumModules["acct"]
    context["modules_arch"] = sumModules["arch"]
    context["modules_bo"] = sumModules["bo"]
    context["modules_fo"] = sumModules["fo"]
    context["modules_risk"] = sumModules['risk']

    return render(request, 'webapp/cases.html', context )

def casedetail(request, caseID):
    resp = viewCase(request,caseID)
    resp = json.loads ( resp.content.decode ( 'utf-8' ) )
    context = {}
    context['case'] = resp['case']
    context["modules_acct"] = sumModules["acct"]
    context["modules_arch"] = sumModules["arch"]
    context["modules_bo"] = sumModules["bo"]
    context["modules_fo"] = sumModules["fo"]
    context["modules_risk"] = sumModules['risk']
    return render(request, 'webapp/case.html', context)

def delete_case(request, caseID, template_name='webapp/confirm_delete.html'):
    case = get_object_or_404(Case, caseID=caseID)
    if request.method == 'POST':
        case.delete()
        return redirect('cases')
    return render(request, template_name, {'object': case})