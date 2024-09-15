catalog = {
    'type': {
        'type_name': '<string>',
        'model': {
            'model_name': '<string>',
            'about_model': {
                'model_title': '<string>',
                'model_about_content': '<text>',
            },
            'specification': {
                'model_configuration': ['<image_url>',],  # list of image urls
                'sleeping_area': '<string>',
                'size': {
                    'size_variant': {
                        'size_variant_length': '<int>',
                        'ize_variant_depth': '<int>',
                    }
                },
                'mechanism': '<string>',
                'deck_base': {
                    'deck_base_variant': {
                        'deck_base_variant_length': '<int>',
                        'deck_base_variant_depth': '<int>',
                    }
                },
                'blueprint': {
                    'left_view': '<image_url>',
                    'top_view': '<image_url>',
                    'top_view_fold_out': '<image_url>',
                    'exploded_view': '<image_url>',
                }
            },
            'color': {
                'name': '<string>',
                'hex_code': '<string>',
                'model_color_image': ['<image_url>',],
            },
        },
    },
}
