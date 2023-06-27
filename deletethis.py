# from app.customer import mapper as customer_mapper

# @customer.route("/register", methods = ["POST"])
# def register():
#     if not request.json:
#         response_object = jsonify({
#             "status" : 'fail',
#             "message": 'Invalid payload'
#         })
#         return response_object,200
#     # check if user us already exists or not
#     user = Customer.query.filter_by(_email_id=request.json['emailId']).first()
#     if user:
#         response_object = jsonify({
#             "status" : 'fail',
#             "message": 'This email is alredy associated with an account. Please sign in or choose another email address.'
#         })
#         return response_object,200
#     else:
#         data = utils.clean_up_request(request.json)
#         try:
#             c = customer_mapper.get_obj_from_request(data,request.json['emailId'])
#         except Exception as e:
#             return common_views.internal_error(constants.view_constants.MAPPING_ERROR)
#         try:
#             db.session.add(c)
#             db.session.commit()

#             # Add Entry for Customer Create Replica
#             try:
#                 create_customer_replica = customer_mapper.get_obj_for_clone_customer(data,request.json['emailId'])
#                 db.session.add(create_customer_replica)
#                 db.session.commit()
#             except Exception as e:
#                 print(e)
#                 return common_views.internal_error(constants.view_constants.DB_TRANSACTION_FAULT)
# #(...)
# #customer made send the email process
#         utils.send_mail(c)
#         #return common_views.as_success(constants.view_constants.USER_REGISTRATION_SUCCESSFUL)
#         booking_response = request.json
#         booking_response['id']=user.id
#         booking_response['uuid']=user._uuid
#         response_object = jsonify({
#             "data":booking_response,
#             "token": str(c.generate_auth_token().decode("utf-8")),
#             "status" : 'success',
#             "message": 'Account created successfully! Please check your email to log in.'
#         })
#         return response_object,200



# #.......
# @customer.route("/oauth/login", methods = ["GET"])
# def oauth_login():
#     type = request.args.get('type')
#     return jsonify({
#         "status": "redirect",
#         "data": {
#             "uri": utils.get_oauth_url(type,common_utils.get_https(request.url_root+"login_callback"))
#             }
#         }), 200
# #.......

# @customer.route("/login/<string:auth_token>", methods = ["GET"])
# def login(auth_token):
#     if not auth_token:
#         return common_views.bad_request(constants.view_constants.REQUEST_PARAMETERS_NOT_SUFFICIENT)
#     c = Customer.verify_auth_token(auth_token)
#     if not c:
#         return common_views.not_authenticated(constants.view_constants.TOKEN_NOT_VALID)
#     user = customer_mapper.get_obj_from_customer_info(c.full_serialize())
#     return jsonify({"user": user, "success": constants.view_constants.USER_LOGGED_IN})

# # ...
# @customer.route("/customerInfo", methods = ["GET"])
# @auth.login_required
# def get_customer():
#     if not g.customer:
#         return common_views.not_authenticated(constants.view_constants.NOT_AUTHENTICATED)
    
#     customer = Customer.query.get(g.customer.id)
#     colors = Colors.query.filter_by(_customer_id=g.customer.id).first()
#     if not colors:
#         colors = Colors(customer_id=g.customer.id)
#         db.session.add(colors)
#         db.session.commit()

#     customer_info = customer.full_serialize()
#     colors_setting = colors.half_serialize()
#     response_object = jsonify({
#         "customer": customer_info,
#         "colors_setting": colors_setting,
#         "status" : 'success',
#         "message": 'Customer fetched'
#     })
#     return response_object,200


# # from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
# # TimedJSONWebSignatureSerializer is deprecated

# # in User, add token---- _otp_secret         = db.Column  (db.Integer) 
# def generate_auth_token(self):
#         serial_token = Serializer(app.config[constants.SECRET_KEY], expires_in = constants.MS.MONTH)
#         return serial_token.dumps({"id": self.id})

# @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(app.config[constants.SECRET_KEY])
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None
#         except BadSignature:
#             return None
#         customer = Customer.query.get(data["id"])
#         return customer

#  @staticmethod
#     def check_email_id(val):
#         return Customer.query.filter(Customer.email_id == val).count() != 0


# # in contants.py:
# # SECRET_KEY = "SECRET_KEY"
# # class MS:
# #    MONTH = 2592000
