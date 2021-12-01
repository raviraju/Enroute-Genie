
# coding: utf-8

# In[1]:

from textblob import TextBlob


# In[5]:

attraction_reviewComments = [
                    "Charming stores and enormous variety of eating establishments. Fun place to walk and browse. When going to Venice Beach, this is a wonderful addition to the experience.",
                    "Abbot Kinney Blvd in Venice Beach is just a perfect example of the boho chic lifestyle Venice and Los Angeles provides. It has a vast array of shops, dining, and culture, all of... read more",
                    "Great shops for window shopping and finding that special thing. Lots and lots of fantastic eateries. We had brunch at Joe's which was excellent.",
                    "I visited on the first Friday of the month looking for some shopping and grab a bit to eat. Boy was I surprised to find a bunch of food trucks everywhere! It turns out, the... read more",
                    "Abbott Kinney has really changed in the last few years, with more small vintage shops, art galleries, and one-of-a-kind boutiques. It is a perfect place to find unusual gifts, or... read more",
                    "What a refreshing and diverse choice of eclectic boutiques, shops and restaurants, totallly laid back. No single chain outlet, Great for a morning brunch, an afternoon stroll or a... read more",
                    "We weren't having a great impression of LA at first but a waitor recommended this area for us to visit. We loved it! Love the graffiti. lots of trendy cute little shops and... read more",
                    "Whenever I am in town, I go check out the Abbot Kinney shops kand enjoy some great eats and coffee. Check out the locals only vibe, cool stores selling fun fashions, home apparel... read more",
                    "The boulevard has become a very ritzy neighborhood that is so pricey, even dot-com millionaires grit their teeth over the prices. Lots of trendy restaurants and unique shops. An... read more",
                    "If you like to eat, you have a lot to pick from on what has become the restaurant row of Venice. Plenty of art shops and clothing choices as well.",
                    "A delight to walk on this street, the selection suits those who have passed the stage of shopping among the large chains. Boutques like Heist and Huset makes it particularly... read more",
                    "Although most gravitate to the boardwalk, the boardwalk shops and food establishments are geared to tourists. Abbott Kinney, is more for the locals, with upscale shopping, and... read more",
                    "Live nearby and have watched this area change a lot! The stores are creative and eclectic. Really the \"Soho\" of LA. Big money has driven out some of the small favorites that us... read more",
                    "Worst experience ever"
                ]


# In[6]:

#len(attraction_reviewComments)
for reviewComment in attraction_reviewComments:
    reviewTextBlob = TextBlob(reviewComment)
    print(reviewComment, reviewTextBlob.sentiment)

