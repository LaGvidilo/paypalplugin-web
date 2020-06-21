#coding: utf-8

import ast
import paypalrestsdk
import logging
class payer(object):
  def __init__(self,client_id="<CLIENT ID HERE>",client_secret="<CLIENT SECRET HERE>", mode_pay="sandbox"):
    paypalrestsdk.configure({
      "mode": mode_pay, # sandbox or live
      "client_id": client_id,
      "client_secret": client_secret})

  def make(self,return_url="http://website.fr/login",cancel_url="http://website.fr",items=[{"name": "item","sku": "item","price": "1.00","currency": "EUR","quantity": 1}],total="1.00",currency="EUR",desc="Buy request."):

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url},
        "transactions": [{
            "item_list": {
                "items": items},
            "amount": {
                "total": total,
                "currency": currency},
            "description": desc}]})

    print({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url},
        "transactions": [{
            "item_list": {
                "items": items},
            "amount": {
                "total": total,
                "currency": currency},
            "description": desc}]})

    if payment.create():
      print("Payment created successfully")
      print(payment)
    else:
      print(payment.error)

    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            # https://github.com/paypal/rest-api-sdk-python/pull/58
            approval_url = str(link.href)
            print("Redirect for approval: %s" % (approval_url))
            return approval_url,payment.id#URL, PAY-ID

  def validate(self,payment_id):
    payment = paypalrestsdk.Payment.find(payment_id)
    payer_id= payment.payer.payer_info.payer_id
    return payment.execute({"payer_id":payer_id})


class panier(object):#sku = "#ID-PRIX-TAILLE-SEXE" 
  def __init__(self,items=[],ship=0):
    #items=[{"name": "item","sku": "item","price": "1.00","currency": "EUR","quantity": 1}]:
    self.items = items
    self.ship = 0

  def init(self):
    self.items = []
    self.ship = 0

  def add(self,name,sku,price,quantity,id_,currency="EUR"):
    self.items.clear()
    self.items.append({"name":name,"sku":sku,"price":str(price),"quantity":int(quantity),"currency":currency})#"id":int(id_),

  def get_all(self):
    return self.items

  def del_item_from_name(self,name):
    for d in self.items:
      if d['name'] == name:
        item = d
    self.items.remove(item)

  def mod_item_from_name(self,name,quantity):
    for d in self.items:
      if d['name'] == name:
        item = d
        item['quantity'] = int(quantity)

  def del_item_from_sku(self,sku):
    for d in self.items:
      if d['sku'] == sku:
        item = d
    self.items.remove(item)

  def mod_item_from_sku(self,sku,quantity):
    for d in self.items:
      if d['sku'] == sku:
        item = d
        item['quantity'] = int(quantity)

  def ret_quantity_item_from_sku(self,sku):
    for d in self.items:
      if d['sku'] == sku:
        item = d
        return item['quantity']

  def mod_ship(self,ship):
    self.ship = ship

  def get_total(self):
    total=0
    for d in self.items:
      total+=float(d['price'])*int(d['quantity'])
    total+=self.ship
    return total

  def verif_no_void(self):
    if len(self.items)>0:
      return True
    else:
      return False

  def align_promo(self,promo=0):
    print("\nAlign promo:>>>")
    total=0.00
    for i in self.items:
      total = total + (float(i['price'])*int(i['quantity']))
    total=float("%.2f" %float(total))
    print("promo:",promo)
    print("total:",total)
    #{"id":int(id_),"name":name,"sku":sku,"price":str(price),"quantity":int(quantity)}
    total_articles = 0
    for i in self.items:
      total_articles+=int(i['quantity'])

    reduc_total = total * (1.0*promo/100)
    ratio = 1.0*reduc_total/total_articles
    print("RATIO:",ratio)
    print("REDUC TOTAL:",reduc_total)
    for i in self.items:
      print("prix:",float(i['price']),"ratio:",ratio)
      i['price'] = float("%.2f" %(float(i['price']) - ratio))
    print("<<<\n")
    return float(total - reduc_total) 







