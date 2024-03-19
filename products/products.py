from flask import Blueprint, render_template, request
from API.api import GetAllProducts, GetSingleProducts, GetAllProductsCategory
products_bp = Blueprint('products_bp', __name__,
    template_folder='templates',
    static_folder='static')

@products_bp.route('/products')
def index():
    data = GetAllProducts()
    l = len(data)
    categories = set(product["category"] for product in data)
    
    return render_template('products/products.html', length = l, products = data, categories = categories)

@products_bp.route('/products/<int:id>')
def detailOfProduct(id):
    data = GetSingleProducts(id)
    #nacteni nazvu kategorie z promenne data do promenne categories
    categories = data["category"]
    #nacteni vsech produktu pres metodu GetAllProductsCategory(categories)
    allProducts = GetAllProductsCategory(categories)
    categoryProduct = [product for product in allProducts if product["category"] == categories]
    l = len(categoryProduct)
    if l > 5:
        l = 5
    filtered_products = [product for product in categoryProduct if product["id"] != id]
    fourProducts = filtered_products[:l]
    return render_template('products/detail.html',length = l, id=id, detailOfProduct=data, features=fourProducts)

@products_bp.route('/products/add', methods=['GET','POST'])
def uploadProduct():
    if request.method == 'POST':
        # Process form data
        product_name = request.form.get('productName')
        product_description = request.form.get('productDescription')
        product_price = request.form.get('productPrice')
        product_category = request.form.get('productCategory')

        # Ensure all required fields are filled
        if not all([product_name, product_description, product_price, product_category]):
            return "Please fill in all the form fields."

        # Generate some random data for demonstration
        random_int = random.randint(100, 1000)
        random_rate = random.uniform(0.0, 5.0)
        image = "static/img/noimage.png"

        # Prepare product data
        product_data = {
            'title': product_name,
            'price': float(product_price),
            'description': product_description,
            'category': product_category,
            'image': image,
            'rating': {'rate':random_rate,'count':random_int}
        }

        # Send data to API
        fakestore_api_url = "https://fakestoreapi.com/products"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(fakestore_api_url, data=json.dumps(product_data), headers=headers)

        # Check response and handle accordingly
        if response.status_code == 201:
            return "Upload successful"
        else:
            return "Upload failed."

    # If it's a GET request, render the form
    MyData = GetAllProducts()
    categories = set(product["category"] for product in MyData)
    sortedCategory = sorted(categories)
    categories_count = {}
    for product in MyData:
        category = product["category"]
        categories_count[category] = categories_count.get(category, 0) + 1
    return render_template('products/new-product.html', products=MyData, categories=sortedCategory, pocetProduktu=categories_count)

if __name__ == '__main__':
    app.run(debug=True)