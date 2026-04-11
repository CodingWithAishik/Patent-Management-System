from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from .models import Copyright, PatentFiled, PatentGranted, IPCategory, IntellectualProperty
from django.forms import ModelForm
from datetime import datetime
import re
import json


# ===== FORMS =====

class CopyrightForm(ModelForm):
    class Meta:
        model = Copyright
        fields = ['sl_no', 'year', 'faculty_students', 'title', 'filing_info', 'inventors']


class PatentFiledForm(ModelForm):
    class Meta:
        model = PatentFiled
        fields = ['sl_no', 'date_of_filing', 'inventors', 'title', 'application_number', 
                  'date_of_publication', 'abstract', 'applicant_name']


class PatentGrantedForm(ModelForm):
    class Meta:
        model = PatentGranted
        fields = ['sl_no', 'granted_patent_no', 'date_of_grant', 'inventors', 'title', 
                  'application_number', 'date_of_publication', 'filing_institute', 'abstract']


# ===== HOMEPAGE =====

def home(request):
    """Homepage with dashboard statistics"""
    context = {
        'total_copyrights': Copyright.objects.count(),
        'total_filed': PatentFiled.objects.count(),
        'total_granted': PatentGranted.objects.count(),
        'recent_copyrights': Copyright.objects.all()[:5],
        'recent_filed': PatentFiled.objects.all()[:5],
        'recent_granted': PatentGranted.objects.all()[:5],
    }
    return render(request, 'patents/home.html', context)


# ===== COPYRIGHT VIEWS =====

def copyright_list(request):
    """List all copyrights with sorting"""
    copyrights = Copyright.objects.all()
    
    # Handle sorting
    sort_by = request.GET.get('sort', '')
    order = request.GET.get('order', 'asc')
    
    if sort_by:
        if order == 'desc':
            sort_by = f'-{sort_by}'
        try:
            copyrights = copyrights.order_by(sort_by)
        except:
            # If invalid field, use default ordering
            pass
    
    context = {
        'copyrights': copyrights,
        'current_sort': request.GET.get('sort', ''),
        'current_order': order
    }
    return render(request, 'patents/copyright_list.html', context)


def copyright_search(request):
    """Search copyrights with dynamic parameters"""
    results = Copyright.objects.all()
    search_performed = False
    
    if request.GET:
        search_performed = True
        year = request.GET.get('year', '').strip()
        faculty = request.GET.get('faculty_students', '').strip()
        title = request.GET.get('title', '').strip()
        inventors = request.GET.get('inventors', '').strip()
        
        if year:
            results = results.filter(year__icontains=year)
        if faculty:
            results = results.filter(faculty_students__icontains=faculty)
        if title:
            results = results.filter(title__icontains=title)
        if inventors:
            results = results.filter(inventors__icontains=inventors)
    
    context = {
        'results': results if search_performed else None,
        'search_performed': search_performed,
        'count': results.count() if search_performed else 0
    }
    return render(request, 'patents/copyright_search.html', context)


def copyright_create(request):
    """Create new copyright"""
    if request.method == 'POST':
        form = CopyrightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patents:copyright_list')
    else:
        form = CopyrightForm()
    return render(request, 'patents/copyright_form.html', {'form': form, 'action': 'Create'})


def copyright_update(request, pk):
    """Update existing copyright"""
    copyright = get_object_or_404(Copyright, pk=pk)
    if request.method == 'POST':
        form = CopyrightForm(request.POST, instance=copyright)
        if form.is_valid():
            form.save()
            return redirect('patents:copyright_list')
    else:
        form = CopyrightForm(instance=copyright)
    return render(request, 'patents/copyright_form.html', {'form': form, 'action': 'Update'})


def copyright_delete(request, pk):
    """Delete copyright"""
    copyright = get_object_or_404(Copyright, pk=pk)
    if request.method == 'POST':
        copyright.delete()
        return redirect('patents:copyright_list')
    return render(request, 'patents/copyright_confirm_delete.html', {'object': copyright})


# ===== PATENT FILED VIEWS =====

def filed_list(request):
    """List all filed patents with sorting"""
    patents = PatentFiled.objects.all()
    
    # Handle sorting
    sort_by = request.GET.get('sort', '')
    order = request.GET.get('order', 'asc')
    
    if sort_by:
        if order == 'desc':
            sort_by = f'-{sort_by}'
        try:
            patents = patents.order_by(sort_by)
        except:
            # If invalid field, use default ordering
            pass
    
    context = {
        'patents': patents,
        'current_sort': request.GET.get('sort', ''),
        'current_order': order
    }
    return render(request, 'patents/filed_list.html', context)


def filed_search(request):
    """Search filed patents with dynamic parameters"""
    results = PatentFiled.objects.all()
    search_performed = False
    
    if request.GET:
        search_performed = True
        date_filing = request.GET.get('date_of_filing', '').strip()
        inventors = request.GET.get('inventors', '').strip()
        title = request.GET.get('title', '').strip()
        app_number = request.GET.get('application_number', '').strip()
        applicant = request.GET.get('applicant_name', '').strip()
        
        if date_filing:
            results = results.filter(date_of_filing__icontains=date_filing)
        if inventors:
            results = results.filter(inventors__icontains=inventors)
        if title:
            results = results.filter(title__icontains=title)
        if app_number:
            results = results.filter(application_number__icontains=app_number)
        if applicant:
            results = results.filter(applicant_name__icontains=applicant)
    
    context = {
        'results': results if search_performed else None,
        'search_performed': search_performed,
        'count': results.count() if search_performed else 0
    }
    return render(request, 'patents/filed_search.html', context)


def filed_create(request):
    """Create new filed patent"""
    if request.method == 'POST':
        form = PatentFiledForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patents:filed_list')
    else:
        form = PatentFiledForm()
    return render(request, 'patents/filed_form.html', {'form': form, 'action': 'Create'})


def filed_update(request, pk):
    """Update existing filed patent"""
    patent = get_object_or_404(PatentFiled, pk=pk)
    if request.method == 'POST':
        form = PatentFiledForm(request.POST, instance=patent)
        if form.is_valid():
            form.save()
            return redirect('patents:filed_list')
    else:
        form = PatentFiledForm(instance=patent)
    return render(request, 'patents/filed_form.html', {'form': form, 'action': 'Update'})


def filed_delete(request, pk):
    """Delete filed patent"""
    patent = get_object_or_404(PatentFiled, pk=pk)
    if request.method == 'POST':
        patent.delete()
        return redirect('patents:filed_list')
    return render(request, 'patents/filed_confirm_delete.html', {'object': patent})


# ===== PATENT GRANTED VIEWS =====

def granted_list(request):
    """List all granted patents with sorting"""
    patents = PatentGranted.objects.all()
    
    # Handle sorting
    sort_by = request.GET.get('sort', '')
    order = request.GET.get('order', 'asc')
    
    if sort_by:
        if order == 'desc':
            sort_by = f'-{sort_by}'
        try:
            patents = patents.order_by(sort_by)
        except:
            # If invalid field, use default ordering
            pass
    
    context = {
        'patents': patents,
        'current_sort': request.GET.get('sort', ''),
        'current_order': order
    }
    return render(request, 'patents/granted_list.html', context)


def granted_search(request):
    """Search granted patents with dynamic parameters"""
    results = PatentGranted.objects.all()
    search_performed = False
    
    if request.GET:
        search_performed = True
        patent_no = request.GET.get('granted_patent_no', '').strip()
        date_grant = request.GET.get('date_of_grant', '').strip()
        inventors = request.GET.get('inventors', '').strip()
        title = request.GET.get('title', '').strip()
        filing_inst = request.GET.get('filing_institute', '').strip()
        
        if patent_no:
            results = results.filter(granted_patent_no__icontains=patent_no)
        if date_grant:
            results = results.filter(date_of_grant__icontains=date_grant)
        if inventors:
            results = results.filter(inventors__icontains=inventors)
        if title:
            results = results.filter(title__icontains=title)
        if filing_inst:
            results = results.filter(filing_institute__icontains=filing_inst)
    
    context = {
        'results': results if search_performed else None,
        'search_performed': search_performed,
        'count': results.count() if search_performed else 0
    }
    return render(request, 'patents/granted_search.html', context)


def granted_create(request):
    """Create new granted patent"""
    if request.method == 'POST':
        form = PatentGrantedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patents:granted_list')
    else:
        form = PatentGrantedForm()
    return render(request, 'patents/granted_form.html', {'form': form, 'action': 'Create'})


def granted_update(request, pk):
    """Update existing granted patent"""
    patent = get_object_or_404(PatentGranted, pk=pk)
    if request.method == 'POST':
        form = PatentGrantedForm(request.POST, instance=patent)
        if form.is_valid():
            form.save()
            return redirect('patents:granted_list')
    else:
        form = PatentGrantedForm(instance=patent)
    return render(request, 'patents/granted_form.html', {'form': form, 'action': 'Update'})


def granted_delete(request, pk):
    """Delete granted patent"""
    patent = get_object_or_404(PatentGranted, pk=pk)
    if request.method == 'POST':
        patent.delete()
        return redirect('patents:granted_list')
    return render(request, 'patents/granted_confirm_delete.html', {'object': patent})


# ===== IP CATEGORY MANAGEMENT VIEWS =====

def _extract_category_fields_from_post(post_data):
    field_definitions = []
    field_count = 0

    while f'field_name_{field_count}' in post_data:
        field_name = post_data.get(f'field_name_{field_count}', '').strip()
        field_label = post_data.get(f'field_label_{field_count}', '').strip()
        field_type = post_data.get(f'field_type_{field_count}', 'text').strip() or 'text'
        field_required = post_data.get(f'field_required_{field_count}') == 'on'
        options_str = post_data.get(f'field_options_{field_count}', '').strip()
        options = [opt.strip() for opt in options_str.split(',') if opt.strip()]

        field_definitions.append(
            {
                'name': field_name,
                'label': field_label,
                'type': field_type,
                'required': field_required,
                'options': options,
            }
        )
        field_count += 1

    return field_definitions


def _validate_category_field_definitions(field_definitions):
    errors = []
    cleaned = []
    allowed_types = {choice[0] for choice in IPCategory.FIELD_TYPES}
    seen_names = set()

    if not field_definitions:
        errors.append('At least one field definition is required.')
        return cleaned, errors

    for idx, field_def in enumerate(field_definitions, start=1):
        field_name = str(field_def.get('name', '')).strip()
        field_label = str(field_def.get('label', '')).strip()
        field_type = str(field_def.get('type', 'text')).strip() or 'text'
        field_required = bool(field_def.get('required', False))
        options = [str(opt).strip() for opt in field_def.get('options', []) if str(opt).strip()]

        if not field_name:
            errors.append(f'Field {idx}: Field name is required.')
            continue

        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', field_name):
            errors.append(
                f'Field {idx}: "{field_name}" is invalid. Use letters, numbers, underscores, and start with a letter.'
            )

        normalized_name = field_name.lower()
        if normalized_name in seen_names:
            errors.append(f'Field {idx}: Duplicate field name "{field_name}" is not allowed.')
        seen_names.add(normalized_name)

        if not field_label:
            errors.append(f'Field {idx}: Field label is required.')

        if field_type not in allowed_types:
            errors.append(f'Field {idx}: "{field_type}" is not a supported field type.')

        if field_type == 'select':
            if not options:
                errors.append(f'Field {idx}: Select fields must define at least one option.')
            elif len(options) != len({opt.lower() for opt in options}):
                errors.append(f'Field {idx}: Select field options must be unique.')

        cleaned_def = {
            'name': field_name,
            'label': field_label,
            'type': field_type,
            'required': field_required,
        }
        if field_type == 'select':
            cleaned_def['options'] = options

        cleaned.append(cleaned_def)

    return cleaned, errors


def _category_form_context(action, category=None, name='', description='', field_definitions=None, schema_errors=None):
    return {
        'action': action,
        'category': category,
        'category_name': name,
        'category_description': description,
        'field_definitions': field_definitions or [],
        'schema_errors': schema_errors or [],
    }

def category_list(request):
    """List all IP categories"""
    categories = IPCategory.objects.all()
    return render(request, 'patents/category_list.html', {'categories': categories})


def category_create(request):
    """Create a new IP category"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        raw_field_definitions = _extract_category_fields_from_post(request.POST)
        field_definitions, schema_errors = _validate_category_field_definitions(raw_field_definitions)

        if not name:
            schema_errors.append('Category name is required.')
        elif IPCategory.objects.filter(name__iexact=name).exists():
            schema_errors.append(f'Category name "{name}" already exists.')

        if not schema_errors:
            IPCategory.objects.create(
                name=name,
                description=description,
                field_definitions=field_definitions,
            )
            return redirect('patents:category_list')

        return render(
            request,
            'patents/category_form.html',
            _category_form_context(
                action='Create',
                name=name,
                description=description,
                field_definitions=raw_field_definitions,
                schema_errors=schema_errors,
            ),
        )

    return render(
        request,
        'patents/category_form.html',
        _category_form_context(action='Create'),
    )


def category_edit(request, pk):
    """Edit an existing IP category"""
    category = get_object_or_404(IPCategory, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        raw_field_definitions = _extract_category_fields_from_post(request.POST)
        field_definitions, schema_errors = _validate_category_field_definitions(raw_field_definitions)

        if not name:
            schema_errors.append('Category name is required.')
        elif IPCategory.objects.filter(name__iexact=name).exclude(pk=category.pk).exists():
            schema_errors.append(f'Category name "{name}" already exists.')

        if not schema_errors:
            category.name = name
            category.description = description
            category.field_definitions = field_definitions
            category.save()
            return redirect('patents:category_list')

        return render(
            request,
            'patents/category_form.html',
            _category_form_context(
                action='Update',
                category=category,
                name=name,
                description=description,
                field_definitions=raw_field_definitions,
                schema_errors=schema_errors,
            ),
        )
    
    return render(
        request,
        'patents/category_form.html',
        _category_form_context(
            action='Update',
            category=category,
            name=category.name,
            description=category.description or '',
            field_definitions=category.field_definitions,
        ),
    )


def category_delete(request, pk):
    """Delete an IP category"""
    category = get_object_or_404(IPCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('patents:category_list')
    return render(request, 'patents/category_confirm_delete.html', {'category': category})


# ===== DYNAMIC IP VIEWS =====

def _validate_dynamic_ip_input(category, post_data):
    cleaned_data = {}
    form_data = {}
    errors = {}

    for field_def in category.field_definitions:
        field_name = str(field_def.get('name', '')).strip()
        if not field_name:
            continue

        field_label = str(field_def.get('label', field_name)).strip() or field_name
        field_type = str(field_def.get('type', 'text')).strip() or 'text'
        required = bool(field_def.get('required', False))
        raw_value = post_data.get(field_name, '')
        value = raw_value.strip() if isinstance(raw_value, str) else ''
        form_data[field_name] = value

        if required and not value:
            errors[field_name] = f'{field_label} is required.'
            continue

        if not value:
            continue

        if field_type == 'number':
            try:
                float(value)
            except ValueError:
                errors[field_name] = f'{field_label} must be a valid number.'
                continue

        if field_type == 'date':
            try:
                datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                errors[field_name] = f'{field_label} must be a valid date (YYYY-MM-DD).'
                continue

        if field_type == 'select':
            options = [str(opt).strip() for opt in field_def.get('options', []) if str(opt).strip()]
            if options and value not in options:
                errors[field_name] = f'{field_label} must be one of the allowed options.'
                continue

        cleaned_data[field_name] = value

    return cleaned_data, form_data, errors

def ip_list(request, category_slug):
    """List all IPs in a category with sorting"""
    category = get_object_or_404(IPCategory, slug=category_slug)
    items = IntellectualProperty.objects.filter(category=category)
    
    # Handle sorting
    sort_by = request.GET.get('sort', '')
    order = request.GET.get('order', 'asc')
    
    if sort_by:
        # For JSON fields, we need to sort differently
        if sort_by.startswith('data__'):
            # Sorting by JSON field
            json_field = sort_by.replace('data__', '')
            if order == 'desc':
                items = sorted(items, key=lambda x: x.data.get(json_field, ''), reverse=True)
            else:
                items = sorted(items, key=lambda x: x.data.get(json_field, ''))
        else:
            # Regular field sorting
            if order == 'desc':
                sort_by = f'-{sort_by}'
            try:
                items = items.order_by(sort_by)
            except:
                pass
    
    context = {
        'category': category,
        'items': items,
        'current_sort': request.GET.get('sort', ''),
        'current_order': order
    }
    return render(request, 'patents/ip_list.html', context)


def ip_create(request, category_slug):
    """Create a new IP in a category"""
    category = get_object_or_404(IPCategory, slug=category_slug)
    
    if request.method == 'POST':
        data, form_data, form_errors = _validate_dynamic_ip_input(category, request.POST)

        if form_errors:
            return render(request, 'patents/ip_form.html', {
                'category': category,
                'action': 'Create',
                'form_data': form_data,
                'form_errors': form_errors,
            })

        if data:
            IntellectualProperty.objects.create(
                category=category,
                data=data
            )
            return redirect('patents:ip_list', category_slug=category_slug)

        return render(request, 'patents/ip_form.html', {
            'category': category,
            'action': 'Create',
            'form_data': form_data,
            'form_errors': {'non_field': 'Please provide at least one field value.'},
        })
    
    return render(request, 'patents/ip_form.html', {
        'category': category,
        'action': 'Create'
    })


def ip_edit(request, category_slug, pk):
    """Edit an existing IP"""
    category = get_object_or_404(IPCategory, slug=category_slug)
    ip_item = get_object_or_404(IntellectualProperty, pk=pk, category=category)
    
    if request.method == 'POST':
        data, form_data, form_errors = _validate_dynamic_ip_input(category, request.POST)

        if form_errors:
            return render(request, 'patents/ip_form.html', {
                'category': category,
                'ip_item': ip_item,
                'action': 'Update',
                'form_data': form_data,
                'form_errors': form_errors,
            })

        if data:
            ip_item.data = data
            ip_item.save()
            return redirect('patents:ip_list', category_slug=category_slug)

        return render(request, 'patents/ip_form.html', {
            'category': category,
            'ip_item': ip_item,
            'action': 'Update',
            'form_data': form_data,
            'form_errors': {'non_field': 'Please provide at least one field value.'},
        })
    
    return render(request, 'patents/ip_form.html', {
        'category': category,
        'ip_item': ip_item,
        'action': 'Update'
    })


def ip_delete(request, category_slug, pk):
    """Delete an IP"""
    category = get_object_or_404(IPCategory, slug=category_slug)
    ip_item = get_object_or_404(IntellectualProperty, pk=pk, category=category)
    
    if request.method == 'POST':
        ip_item.delete()
        return redirect('patents:ip_list', category_slug=category_slug)
    
    return render(request, 'patents/ip_confirm_delete.html', {
        'category': category,
        'ip_item': ip_item
    })


def ip_search(request, category_slug):
    """Search IPs in a category"""
    category = get_object_or_404(IPCategory, slug=category_slug)
    items = IntellectualProperty.objects.filter(category=category)
    
    # Build search query
    if request.method == 'GET' and request.GET:
        query_parts = []
        for field_def in category.field_definitions:
            field_name = field_def['name']
            search_value = request.GET.get(field_name, '').strip()
            
            if search_value:
                # Search in JSON data field
                # Filter items where data contains the field with matching value
                items = items.filter(
                    **{f'data__{field_name}__icontains': search_value}
                )
    
    return render(request, 'patents/ip_search.html', {
        'category': category,
        'items': items
    })

