from typing import List, Optional
import time

from fastapi import APIRouter, Cookie, Form, Header, Response, status
from fastapi.responses import HTMLResponse, PlainTextResponse

from custom_log import log


router = APIRouter(
    prefix='/product',
    tags=['product']
)


products = ['watch', 'camera', 'phone']


async def time_consuming_functionality():
    time.sleep(5)
    return 'OK'


@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get('/all')
async def get_all_products():
    # log('MyAPI', 'Call to get all products')
    # await time_consuming_functionality()
    # return products
    data = ' '.join(products)
    response = Response(content=data, media_type='text/plain')
    # different types of response:
    #   - plain text; - xml; - html; - files; - streaming;

    response.set_cookie(key='test_cookie', value='test_cookie_value')
    return response


@router.get('/withheader')
def get_products(
    response: Response,
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None)
):
    if custom_header:
        response.headers['custom-response-header'] = ', '.join(custom_header)
    return {
        'data': products,
        'custom_deader': custom_header,
        'my_cookie': test_cookie
    }


@router.get(
    '/{id}',
    responses={
        200: {
            'content': {
                'text/html': {
                    'example': '<div>Product</div>'
                }
            },
            'description': 'Returns the HTML for an object'
        },
        400: {
            'content': {
                'text/plain': {
                    'example': 'Product not available'
                }
            },
            'description': 'A cleartext error message'
        }
    }
)
def get_product(id: int):
    if id > len(products):
        out = 'Product not available'
        return PlainTextResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=out,
            media_type='text/plain'
        )
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content=out, media_type='text/html')
