from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import TestForm, PageForm, SnippetVariantFormSet, SnippetVariant
from .models import Page, SnippetVariant, Test
from django.shortcuts import get_object_or_404, render
from django.db import transaction


def create_test(request):
    if request.method == "POST":
        test_form = TestForm(request.POST)
        page_form = PageForm(request.POST)
        variant_formset = SnippetVariantFormSet(request.POST, queryset=SnippetVariant.objects.none())

        if test_form.is_valid() and page_form.is_valid() and variant_formset.is_valid():
            try:
                with transaction.atomic():
                    page = page_form.save(commit=False)
                    page.user = request.user
                    page.save()

                    test = test_form.save(commit=False)
                    test.page = page
                    test.status = "created"
                    test.save()

                    for form in variant_formset:
                        if form.has_changed():  # ← Only save if user actually entered something
                            variant = form.save(commit=False)
                            variant.page = page
                            variant.save()

                    # Redirect to dashboard
                    return redirect("dashboard:dashboard")
            except Exception:
                pass
    else:
        test_form = TestForm()
        page_form = PageForm()
        variant_formset = SnippetVariantFormSet(queryset=SnippetVariant.objects.none())

    return render(request, "testt/create_test.html", {
        "test_form": test_form,
        "page_form": page_form,
        "variant_formset": variant_formset,
    })


def detail_test(request, test_id):
    detail_test = get_object_or_404(Test, pk=test_id)
    return render(request, 'testt/detail_test.html', {'detail_test': detail_test})


@require_http_methods(["POST"])
def update_status(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    new_status = request.POST.get('status')

    if new_status in dict(Test.STATUS_CHOICES):
        test.status = new_status
        test.save()

    csrf_token = get_token(request)

    select_html = f'''
    <select class="form-control form-control-sm"
            hx-post="{request.path}"
            hx-trigger="change"
            hx-target="this"
            hx-swap="outerHTML"
            hx-headers='{{"X-CSRFToken": "{csrf_token}"}}'
            name="status">
    '''

    for value, label in Test.STATUS_CHOICES:
        selected = 'selected' if value == test.status else ''
        select_html += f'<option value="{value}" {selected}>{label}</option>'

    select_html += '</select>'
    print(csrf_token)

    return HttpResponse(select_html)


@login_required()
@require_http_methods(['DELETE'])
def delete_test(request, test_id):
    get_test = get_object_or_404(Test, pk=test_id)
    page = get_test.page
    if get_test.page.user != request.user:
        return HttpResponseForbidden('You cannot delete this')
    else:
        page.delete()
    return HttpResponse(status=204)

