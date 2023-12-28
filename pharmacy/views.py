import email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hospital.models import Patient
from pharmacy.models import Medicine, Cart, Order
from .utils import searchMedicines
from django.views.decorators.csrf import csrf_exempt


# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver


# Create your views here.

# function to return views for the urls

@csrf_exempt
@login_required(login_url="login")
def pharmacy_single_product(request,pk):
     if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.get(serial_number=pk)
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'order': order, 'orders': orders}
            return render(request, 'pharmacy/product-single.html',context)
        else:
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'orders': orders}
            return render(request, 'pharmacy/product-single.html',context)
     else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def pharmacy_shop(request):
    if request.user.is_authenticated and request.user.is_patient:
        
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        
        medicines, search_query = searchMedicines(request)
        
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'order': order, 'orders': orders, 'search_query': search_query}
            return render(request, 'Pharmacy/shop.html', context)
        else:
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'orders': orders, 'search_query': search_query}
            return render(request, 'Pharmacy/shop.html', context)
    
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def checkout(request):
    return render(request, 'pharmacy/checkout.html')

@csrf_exempt
@login_required(login_url="login")
def add_to_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        
        item = get_object_or_404(Medicine, pk=pk)
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                # messages.warning(request, "This item quantity was updated!")
                context = {'patient': patient,'medicines': medicines, 'order': order}
                return render(request, 'pharmacy/shop.html', context)
            
            else:
                order.orderitems.add(order_item[0])
                # messages.warning(request, "This item is added to your cart!")
                context = {'patient': patient,'medicines': medicines,'order': order}
                return render(request, 'pharmacy/shop.html', context)
        else:
            order = Order(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            # messages.warning(request, "This item is added to your cart!")
            context = {'patient': patient,'medicines': medicines,'order': order}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="login")
def cart_view(request):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'carts': carts,'order': order}
            return render(request, 'Pharmacy/cart.html', context)
        else:
            messages.warning(request, "You don't have any item in your cart!")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html') 

@csrf_exempt
@login_required(login_url="login")
def remove_from_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was remove from your cart!")
                context = {'carts': carts,'order': order}
                return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.info(request, "This item was not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 


@csrf_exempt
@login_required(login_url="login")
def increase_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.warning(request, f"{item.name} is not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.warning(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 


@csrf_exempt
@login_required(login_url="login")
def decrease_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:
         
        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.name} item has been removed from your cart")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.info(request, f"{item.name} is not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 
    
# --------------------------------------------->algorithm for cosine sin 
# import torch
# from PIL import Image
# from torchvision import transforms
# import json
# from .models import Product, FeatureVector

# # Function to extract features from an image using a pre-trained model
# def extract_features_from_image(image_path):
#     image = Image.open(image_path).convert("RGB")
#     transform = transforms.Compose([
#         transforms.Resize((224, 224)),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ])
#     image = transform(image).unsqueeze(0)

#     model = torch.hub.load("pytorch/vision", "resnet18", pretrained=True)
#     model.eval()

#     with torch.no_grad():
#         features = model(image).squeeze().numpy().tolist()

#     return features

# # Function to create feature vectors for products
# def create_feature_vectors():
#     products = Product.objects.all()

#     for product in products:
#         # Check if a feature vector already exists for the product
#         if FeatureVector.objects.filter(product=product).exists():
#             continue

#         # Extract features from the product's image
#         feature_vector = extract_features_from_image(product.image.D:\All abot project\cProject\HealthStack-System\static\images\medicines)

#         # Create or update the feature vector for the product
#         feature_vector_obj, created = FeatureVector.objects.get_or_create(
#             product=product, defaults={"feature_vector": json.dumps(feature_vector)}
#         )

#         # Save the feature vector object
#         feature_vector_obj.save()

# # Call the function to create feature vectors for products
# create_feature_vectors()


























    


#     def extract_features_from_image(image_D:\All abot project\cProject\HealthStack-System\static\images\medicines):
    
#     image = Image.open(image_path).convert("RGB")
#     transform = transforms.Compose(
#         [
#             transforms.Resize((224,224)),
#             transforms.ToTensor(),
#             transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#         ]
#     )
#     image = transform(image).unsqueeze(0)

    
#     model = torch.hub.load("pytorch/vision", "resnet18", pretrained=True)
#     model.eval()


#     with torch.no_grad():
#         features = model(image).squeeze().numpy().tolist()

#     return features


# def create_feature_vectors():
    
#     products = Product.objects.all()

#     for product in products:
        
#         if FeatureVector.objects.filter(product=product).exists():
#             continue  

   
#         feature_vector = extract_features_from_image(product.image.D:\All abot project\cProject\HealthStack-System\static\images\medicines)

     
#         feature_vector_obj, created = FeatureVector.objects.get_or_create(
#             product=product, defaults={"feature_vector": json.dumps(feature_vector)}
#         )

      
#         feature_vector_obj.save()

    



# Create your views here.
