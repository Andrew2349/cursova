import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver_email, subject, html_content):
    sender_email = 'andrusha2349@gmail.com'
    sender_password = 'tyxc ofbj gbiw cauu'
    message = MIMEMultipart('related')
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(html_content, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(message)
    server.close()


def send_order_details(order):
    html = f'''
    <div class="container px-4 px-lg-5 my-5">
            <div class="row gx-4 gx-lg-5 align-items-center">
                <div class="col-mb-2">
                    <h1 class="fw-bold mb-4 order">Your order</h1>
                </div>
                <div class="col-md-5" style="width:300px; height:220px;" >
                    <img class="img-fluid car-img" style="width: 100%;height: 100%;object-fit: cover;object-position: center;" src="{order.car.img}" alt="Car Image">
                </div>
                <div class="col-md-5">
                    <h3><strong class="text-dark">Purchaser</strong>: {order.custom_user.fullname}</h3>
                    <h3><strong class="text-dark">Email</strong>: {order.custom_user.email}</h3>
                    <h3><strong class="text-dark">Phone number</strong>: {order.custom_user.phone}</h3>
                    <h3><strong class="text-dark">Car</strong>: {order.car.brand} {order.car.model}</h3>
                    <div class="price-box">
                        <h3><strong class="text-dark">Price</strong>: {order.car.final_price()} $</h3> 
                    </div>
                    <h3><strong class="text-dark">Date</strong>: {order.date}</h3>
                </div>
            </div>
        </div>
        '''
    send_email(order.custom_user.email, f"You made order №{order.id}", html)
