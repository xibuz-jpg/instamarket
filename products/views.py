from products.forms import CategoryForm


def category_add(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = CategoryForm()

    return render(request, 'core/category_form.html', {
        'form': form,
        'title': "Bo'lim qo'shish"
    })
