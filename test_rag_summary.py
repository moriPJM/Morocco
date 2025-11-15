from streamlit_app import get_ai_response

# Minimal ai_service to force fallback path
ai_service = {
    'available': False,
    'knowledge_base': {
        'country_info': {'name':'モロッコ王国','capital':'ラバト','largest_city':'カサブランカ','population':'3700万','languages':['アラビア語','フランス語'],'currency':'MAD','religion':'イスラム教'},
        'cultural_context': {'berber_heritage':'ベルベル','islamic_influence':'あり','andalusian_legacy':'あり','french_colonial':'あり'},
        'travel_tips': {'best_seasons':{'spring':'3-5月','summer':'6-8月','autumn':'9-11月','winter':'12-2月'}, 'cultural_etiquette':{'greetings':'アッサラーム','dress_code':'控えめ','photography':'許可'}}
    },
    'fallback_responses': {'general':'モロッコは多様な文化と美しい景観を持つ国です。訪問時は服装や文化的配慮に注意してください。'}
}

prompt = 'マラケシュでおすすめの食べ物は？'
print('Prompt:', prompt)
resp = get_ai_response(prompt, ai_service)
print('\nResponse:\n', resp)
