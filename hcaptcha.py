from playwright.async_api import async_playwright
import asyncio,re,time,httpx,random




async def main():
    async with async_playwright() as p:
        # Launch the browser in non-headless mode

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to the page
        await page.goto("https://accounts.hcaptcha.com/demo")

        # Wait for the hCaptcha iframe to be loaded and then switch to it
        frame_element = await page.wait_for_selector("//iframe[contains(@src, 'hcaptcha')]")
        frame = await frame_element.content_frame()

       
        await frame.click('//*[@id="checkbox"]')
        while True:


            await page.wait_for_selector("//iframe[contains(@title, 'hCaptcha challenge')]")
            challenge_frame_element = await page.wait_for_selector("//iframe[contains(@title, 'hCaptcha challenge')]")
            challenge_frame = await challenge_frame_element.content_frame()



            
            time.sleep(3)
        
            try:
             await challenge_frame.wait_for_selector('xpath=/html/body/div/div[1]/div/div/div[1]/div[1]/div[1]/h2/span', timeout=1000)
             prompt_text = await challenge_frame.text_content('xpath=/html/body/div/div[1]/div/div/div[1]/div[1]/div[1]/h2/span')

            except :
                prompt_text=None

                if prompt_text == None:
                   print('changing captcha con 1')
                   
                   
                   random_x = 619
                   random_y = 240

                 
                   await page.mouse.click(random_x, random_y)
                   frame_element = await page.wait_for_selector("//iframe[contains(@src, 'hcaptcha')]")
                   frame = await frame_element.content_frame()
                   await frame.click('//*[@id="checkbox"]')
                   
                   continue


            image_locator = challenge_frame.locator('//div[contains(@class, "task-image")]/div[@class="wrapper"]/div[contains(@class, "image")]')
        
       
            image_count = await image_locator.count()
            
            if 'objects' in prompt_text.lower():
                if 'pairs' in prompt_text:
                    ques='the image object is it with their identical pairs or not?give answer in yes or no only'
                elif 'crafted' in prompt_text:
                    ques='the image machine/animal can it be made by humans or not?give answer in yes or no only'
                elif 'performed' in prompt_text:
                    ques='the image object can it be performed together with other human or not?give answer in yes or no only'
                elif 'pictures' in prompt_text:
                    ques='the image object can i able to take picture like camera with this?give answer in yes or no only'
                elif 'ride' in prompt_text:
                    ques='the image object can i able to ride?give anwser in yes or no only'
                elif 'backpack'in prompt_text:
                    ques='the image object can it fit in backpack?give answer in yes or no only'
            elif 'activities' in prompt_text.lower():
                if 'performed' in prompt_text:
                    ques='the image object can it be performed with 2 human together?give answer in yes or no only'

            else:
                ques='None'

            print(prompt_text)
           
            answer=[]
            
            time.sleep(1)

            print(ques)
            for i in range(image_count):
                image_div = image_locator.nth(i)
                style_attr = await image_div.get_attribute('style')
                url_match = re.search(r'url\("(.+?)"\)', style_attr)
            
                if url_match:
                    image_url = url_match.group(1)

                    url = "https://replicate.com/api/models/yorickvp/llava-13b/versions/b5f6212d032508382d61ff00469ddda3e32fd8a0e75dc39d8a4191bb742157fb/predictions"

                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
                        "Accept": "application/json",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Referer": "https://replicate.com/yorickvp/llava-13b",
                        "Content-Type": "application/json",
                        "Origin": "https://replicate.com",
                        "Connection": "keep-alive",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
           
           
                    }

                    data = {
                        "input": {
                            "image": str(image_url),
                            "max_tokens": 1024,
                            "prompt": str(ques),
                            "temperature": 0.2,
                            "top_p": 1
                        },
                        "stream": False
            }
                    response = httpx.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    ids = response.json().get('id')

                    if ids:
                        while True:
                            status = httpx.get(f'https://replicate.com/api/predictions/{ids}', headers=headers)
                            status.raise_for_status()
                            progress = status.json().get('status')
                            print(progress)
                            if progress != 'processing':
                                output = status.json().get('output')
                                if output:
                                    full_description = ''.join(output)
                                    print(full_description)
                                    break


                   
                    
                    if 'yes' in full_description.lower():
                   
                          answer.append(i + 1)

                

                   
            #total_yes=[1,2,9]

                
            print(answer)

                

       
            #total_yes = len(answer)

            image_locator = challenge_frame.locator('//div[contains(@class, "task-image")]')
            print(image_locator)
            image_count = await image_locator.count()
            print(f"Found {image_count} challenge images.")

            if image_count < 9:
                   print('changing captcha con 2')
                 
                   
                  
                   random_x = 619
                   random_y = 240
                   print(random_x,random_y)
                    # Perform the mouse click at the random coordinates
                   await page.mouse.click(random_x, random_y)
                   frame_element = await page.wait_for_selector("//iframe[contains(@src, 'hcaptcha')]")
                   frame = await frame_element.content_frame()
                   await frame.click('//*[@id="checkbox"]')
                   continue

            for index in answer:
              
                await image_locator.nth(index - 1).click()
                print(f"Clicked on image {index}")
    




            #final click
            final_div_xpath = 'xpath=/html/body/div/div[3]/div[3]'

        
            await challenge_frame.wait_for_selector(final_div_xpath, state="visible")
            await challenge_frame.click(final_div_xpath)

            try:
                error_selector = '.error-text'
                error_message_element = await challenge_frame.wait_for_selector(error_selector, state="visible", timeout=5000)
                error_message = await error_message_element.text_content()
              
            except:
                error_message = None

            if error_message == None:
                break

          
            try:
               
                    xpath_selector = '//*[@class="check"]'

                    # Check if the element is visible
                    is_visible = await frame.is_visible(xpath_selector)

                    print(f"Is the element visible? {is_visible}")

                    await frame.wait_for_selector(xpath_selector, state='visible')

                    # Re-check visibility after the operation
                    is_visible_after_operation = await frame.is_visible(xpath_selector)

                    print(f"Is the element visible after operation? {is_visible_after_operation}")
                    if is_visible_after_operation == True:
                        print("Solved captchs")
                        time.sleep(1)
                        await page.reload()
                        break


            except Exception as error:
                print(error)
                print('retry')

        
        
        
asyncio.run(main())
