RECIPES_DATA = {
    'Breakfast': [
        {
            'title': 'Aloo Paratha',
            'description': 'A popular Indian flatbread stuffed with spiced mashed potatoes.',
            'cooking_time': 30,
            'servings': 2,
            'difficulty': 'medium',
            'ingredients': [
                {'name': 'Whole wheat flour', 'quantity': '2', 'unit': 'cups'},
                {'name': 'Potatoes', 'quantity': '3', 'unit': 'medium'},
                {'name': 'Cumin seeds', 'quantity': '1', 'unit': 'tsp'},
                {'name': 'Red chili powder', 'quantity': '1', 'unit': 'tsp'},
                {'name': 'Salt', 'quantity': 'to taste', 'unit': ''},
            ],
            'steps': [
                'Boil and mash the potatoes with spices.',
                'Make dough with whole wheat flour.',
                'Stuff the dough with potato mixture.',
                'Roll out and cook on a hot griddle.',
            ]
        },
        {
            'title': 'Shakshuka',
            'description': 'A Middle Eastern breakfast dish of eggs poached in a spicy tomato sauce.',
            'cooking_time': 25,
            'servings': 4,
            'difficulty': 'easy',
            'ingredients': [
                {'name': 'Eggs', 'quantity': '6', 'unit': ''},
                {'name': 'Tomatoes', 'quantity': '6', 'unit': 'large'},
                {'name': 'Onion', 'quantity': '1', 'unit': 'large'},
                {'name': 'Bell peppers', 'quantity': '2', 'unit': ''},
                {'name': 'Garlic', 'quantity': '4', 'unit': 'cloves'},
            ],
            'steps': [
                'Sauté onions and peppers.',
                'Add tomatoes and spices.',
                'Create wells and crack eggs.',
                'Cover and cook until eggs are done.',
            ]
        },
        {
            'title': 'Avocado Toast',
            'description': 'A healthy and trendy breakfast with mashed avocado on toasted bread.',
            'cooking_time': 10,
            'servings': 1,
            'difficulty': 'easy',
            'ingredients': [
                {'name': 'Bread', 'quantity': '2', 'unit': 'slices'},
                {'name': 'Avocado', 'quantity': '1', 'unit': 'ripe'},
                {'name': 'Lemon juice', 'quantity': '1', 'unit': 'tbsp'},
                {'name': 'Red pepper flakes', 'quantity': '1/4', 'unit': 'tsp'},
                {'name': 'Salt', 'quantity': 'to taste', 'unit': ''},
            ],
            'steps': [
                'Toast the bread until golden.',
                'Mash the avocado with lemon juice and salt.',
                'Spread the avocado mixture on toast.',
                'Sprinkle with red pepper flakes.',
            ]
        },
    ],
    'Main Course': [
        {
            'title': 'Chicken Curry',
            'description': 'A classic Indian curry with tender chicken in a spiced tomato-based sauce.',
            'cooking_time': 45,
            'servings': 4,
            'difficulty': 'medium',
            'ingredients': [
                {'name': 'Chicken', 'quantity': '1', 'unit': 'kg'},
                {'name': 'Onions', 'quantity': '2', 'unit': 'large'},
                {'name': 'Tomatoes', 'quantity': '3', 'unit': 'large'},
                {'name': 'Ginger-garlic paste', 'quantity': '2', 'unit': 'tbsp'},
                {'name': 'Curry powder', 'quantity': '2', 'unit': 'tbsp'},
            ],
            'steps': [
                'Marinate chicken with spices.',
                'Sauté onions until golden.',
                'Add tomatoes and cook until soft.',
                'Add chicken and simmer until done.',
            ]
        },
        {
            'title': 'Bibimbap',
            'description': 'A Korean rice bowl topped with vegetables, meat, and gochujang sauce.',
            'cooking_time': 40,
            'servings': 2,
            'difficulty': 'medium',
            'ingredients': [
                {'name': 'Rice', 'quantity': '2', 'unit': 'cups'},
                {'name': 'Beef', 'quantity': '200', 'unit': 'g'},
                {'name': 'Carrots', 'quantity': '1', 'unit': 'large'},
                {'name': 'Spinach', 'quantity': '2', 'unit': 'cups'},
                {'name': 'Gochujang', 'quantity': '2', 'unit': 'tbsp'},
            ],
            'steps': [
                'Cook rice according to package instructions.',
                'Stir-fry vegetables separately.',
                'Cook beef with soy sauce and sesame oil.',
                'Assemble bowl with rice, vegetables, and beef.',
            ]
        },
    ],
    'Healthy & Vegetarian': [
        {
            'title': 'Quinoa Salad',
            'description': 'A nutritious salad with quinoa, fresh vegetables, and a light dressing.',
            'cooking_time': 20,
            'servings': 4,
            'difficulty': 'easy',
            'ingredients': [
                {'name': 'Quinoa', 'quantity': '1', 'unit': 'cup'},
                {'name': 'Cucumber', 'quantity': '1', 'unit': 'large'},
                {'name': 'Cherry tomatoes', 'quantity': '1', 'unit': 'cup'},
                {'name': 'Red onion', 'quantity': '1/2', 'unit': ''},
                {'name': 'Lemon juice', 'quantity': '2', 'unit': 'tbsp'},
            ],
            'steps': [
                'Cook quinoa according to package instructions.',
                'Chop vegetables into bite-sized pieces.',
                'Mix cooked quinoa with vegetables.',
                'Dress with lemon juice and olive oil.',
            ]
        },
    ],
    'Soups & Stews': [
        {
            'title': 'Tom Yum Soup',
            'description': 'A hot and sour Thai soup with shrimp and mushrooms.',
            'cooking_time': 30,
            'servings': 4,
            'difficulty': 'medium',
            'ingredients': [
                {'name': 'Shrimp', 'quantity': '300', 'unit': 'g'},
                {'name': 'Mushrooms', 'quantity': '200', 'unit': 'g'},
                {'name': 'Lemongrass', 'quantity': '2', 'unit': 'stalks'},
                {'name': 'Lime leaves', 'quantity': '4', 'unit': ''},
                {'name': 'Fish sauce', 'quantity': '2', 'unit': 'tbsp'},
            ],
            'steps': [
                'Prepare the broth with lemongrass and lime leaves.',
                'Add mushrooms and cook until tender.',
                'Add shrimp and cook until pink.',
                'Season with fish sauce and lime juice.',
            ]
        },
    ],
    'Desserts': [
        {
            'title': 'Gulab Jamun',
            'description': 'Sweet, spongy milk-solid balls soaked in rose-flavored sugar syrup.',
            'cooking_time': 45,
            'servings': 6,
            'difficulty': 'medium',
            'ingredients': [
                {'name': 'Milk powder', 'quantity': '1', 'unit': 'cup'},
                {'name': 'All-purpose flour', 'quantity': '1/4', 'unit': 'cup'},
                {'name': 'Ghee', 'quantity': '1', 'unit': 'tbsp'},
                {'name': 'Sugar', 'quantity': '2', 'unit': 'cups'},
                {'name': 'Cardamom', 'quantity': '4', 'unit': 'pods'},
            ],
            'steps': [
                'Mix milk powder, flour, and ghee to make dough.',
                'Shape into small balls.',
                'Deep fry until golden brown.',
                'Soak in hot sugar syrup.',
            ]
        },
    ],
    'Drinks': [
        {
            'title': 'Masala Chai',
            'description': 'Traditional Indian spiced tea with milk.',
            'cooking_time': 15,
            'servings': 2,
            'difficulty': 'easy',
            'ingredients': [
                {'name': 'Black tea leaves', 'quantity': '2', 'unit': 'tsp'},
                {'name': 'Milk', 'quantity': '1', 'unit': 'cup'},
                {'name': 'Ginger', 'quantity': '1', 'unit': 'inch'},
                {'name': 'Cardamom', 'quantity': '2', 'unit': 'pods'},
                {'name': 'Sugar', 'quantity': 'to taste', 'unit': ''},
            ],
            'steps': [
                'Crush ginger and cardamom.',
                'Boil water with spices.',
                'Add tea leaves and simmer.',
                'Add milk and sugar, bring to boil.',
            ]
        },
    ],
} 