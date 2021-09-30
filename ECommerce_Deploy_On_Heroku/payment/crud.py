import stripe

from base_url import base_url


def payment_process(total_price):

    session= stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items= [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': "Your Bills"
                },
                'unit_amount_decimal': "{:.2f}".format(total_price*100)
            },
            'quantity': 1
        }],
        mode= 'payment',
        success_url= base_url+'/payment/done',
        cancel_url=base_url + '/payment/canceled'
    )

    return session