import requests
import json

SPB_STORE_ID = 15
MOSCOW_STORE_ID = 10

SLUGS = ['kolbasy-vetchina', 'shokolad-batonchiki']

result = []
for store_id in [SPB_STORE_ID, MOSCOW_STORE_ID]:
    for slug in SLUGS:
        json_data = {
            'query': '\n  query Query($storeId: Int!, $slug: String!, $attributes:[AttributeFilter], $filters: [FieldFilter], $from: Int!, $size: Int!, $sort: InCategorySort, $in_stock: Boolean, $eshop_order: Boolean, $is_action: Boolean, $priceLevelsOnline: Boolean) {\n    category (storeId: $storeId, slug: $slug, inStock: $in_stock, eshopAvailability: $eshop_order, isPromo: $is_action, priceLevelsOnline: $priceLevelsOnline) {\n      id\n      name\n      slug\n      id\n      parent_id\n      meta {\n        description\n        h1\n        title\n        keywords\n      }\n      disclaimer\n      description {\n        top\n        main\n        bottom\n      }\n      breadcrumbs {\n        category_type\n        id\n        name\n        parent_id\n        parent_slug\n        slug\n      }\n      promo_banners {\n        id\n        image\n        name\n        category_ids\n        type\n        sort_order\n        url\n        is_target_blank\n        analytics {\n          name\n          category\n          brand\n          type\n          start_date\n          end_date\n        }\n      }\n\n\n      dynamic_categories(from: 0, size: 9999) {\n        slug\n        name\n        id\n        category_type\n        dynamic_product_settings {\n          attribute_id\n          max_value\n          min_value\n          slugs\n          type\n        }\n      }\n      filters {\n        facets {\n          key\n          total\n          filter {\n            id\n            hru_filter_slug\n            is_hru_filter\n            is_filter\n            name\n            display_title\n            is_list\n            is_main\n            text_filter\n            is_range\n            category_id\n            category_name\n            values {\n              slug\n              text\n              total\n            }\n          }\n        }\n      }\n      total\n      prices {\n        max\n        min\n      }\n      pricesFiltered {\n        max\n        min\n      }\n      products(attributeFilters: $attributes, from: $from, size: $size, sort: $sort, fieldFilters: $filters)  {\n        health_warning\n        limited_sale_qty\n        id\n        slug\n        name\n        name_highlight\n        article\n        new_status\n        main_article\n        main_article_slug\n        is_target\n        category_id\n        category {\n          name\n        }\n        url\n        images\n        pick_up\n        rating\n        icons {\n          id\n          badge_bg_colors\n          rkn_icon\n          caption\n          type\n          is_only_for_sales\n          caption_settings {\n            colors\n            text\n          }\n          sort\n          image_svg\n          description\n          end_date\n          start_date\n          status\n        }\n        manufacturer {\n          name\n        }\n        packing {\n          size\n          type\n        }\n        stocks {\n          value\n          text\n          scale\n          eshop_availability\n          prices_per_unit {\n            old_price\n            offline {\n              price\n              old_price\n              type\n              offline_discount\n              offline_promo\n            }\n            price\n            is_promo\n            levels {\n              count\n              price\n            }\n            online_levels {\n              count\n              price\n              discount\n            }\n            discount\n          }\n          prices {\n            price\n            is_promo\n            old_price\n            offline {\n              old_price\n              price\n              type\n              offline_discount\n              offline_promo\n            }\n            levels {\n              count\n              price\n            }\n            online_levels {\n              count\n              price\n              discount\n            }\n            discount\n          }\n        }\n      }\n      argumentFilters {\n        eshopAvailability\n        inStock\n        isPromo\n        priceLevelsOnline\n      }\n    }\n  }\n',
            'variables': {
                'isShouldFetchOnlyProducts': True,
                'slug': slug,
                'storeId': store_id,
                'sort': 'default',
                'size': 100000000,
                'from': 0,
                'filters': [
                    {
                        'field': 'main_article',
                        'value': '0',
                    },
                ],
                'attributes': [],
                'in_stock': True,
                'eshop_order': False,
            },
        }

        response = requests.post('https://api.metro-cc.ru/products-api/graph', json=json_data).json()
        for product in response['data']['category']['products']:
            new_product = {
                "id":product['id'],
                "name":product['name'],
                "price":product['stocks'][0]['prices']['price'] if  not product['stocks'][0]['prices']['is_promo'] else product['stocks'][0]['prices']['old_price'],
                "promo_price":product['stocks'][0]['prices']['price'] if product['stocks'][0]['prices']['is_promo'] else product['stocks'][0]['prices']['old_price'],
                "url":"https://online.metro-cc.ru" + product['url'],
                "brand":product['manufacturer']['name']
            }
            result.append(new_product)

json.dump(result, open("ouput.json", "wt", encoding="utf-8"), ensure_ascii=False, indent=4)
