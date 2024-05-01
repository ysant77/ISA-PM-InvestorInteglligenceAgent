import tagui as t

# Get Competitors from Google
def scrape_competitors(company):
    try:
        # Get Competitors from Google
        t.init(visual_automation = True) # visual automation if keyboard automation required in subsequent code
        t.url('https://www.google.com/') # go to google website
        t.type('//*[@name="q"]', 'who are the top 5 company competitors of ' + company + '[enter]')
        t.click('//div[contains(@class,"FPdoLc")]//input[1]')  # Click the search button

        top_competitors = []

        # Loop from 1 to 3 inclusive
        for i in range(1, 4):
            # Construct XPath expressions for top competitors
            top_competitors_xpath = '//*[@jsname="ibnC6b"][' + str(i) + ']//div[@data-attrid="BreadthFirstSRP"]'

            # Read top competitors using TagUI's t.read() function
            top_competitors.append(t.read(top_competitors_xpath))

        return top_competitors

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


# Scrape from ratings (Step 2)
# This step shall take place after logging in and searched company so that rating is available from searched company
def scrape_rating():
    try:
        company_rating = t.read("//p[contains(@class,'rating-headline-average_rating')][text()]") # employer overview rating
        # print (company_rating)
        job_recommendation = t.read("//p[@data-test='recommendToFriend'][text()]").split(' would')[0] # recommend to friend rating
        # print (job_recommendation)
        ceo_approval = t.read("//p[contains(@class,'review-overview_ceoApproval')][text()]").split(' approve')[0] # ceo approval rating
        # print (ceo_approval)

        t.wait(1)
        t.click('//div[contains(@class,"review-overview_buttonContainer")]/button') # extend to show more insights
        t.wait(2)
        cat_rate_xpath = "//div[contains(@class,'review-overview_industryAverageContainer')]/div[contains(@class,'review-overview_ratingItem')]"
        cat_arr = []
        cat_rate_arr = []
        for i in range(1,7):
            cat_arr.append(t.read(f'{cat_rate_xpath}[{i}]/p[contains(@class,"review-overview_ratingLabel")]')) # Diversity, Work/Life balance, etc.
            cat_rate_arr.append(float(t.read(f'{cat_rate_xpath}[{i}]/p[contains(@class,"review-overview_rating__dp_IU")]'))) # 4.3
        t.wait(1)

        return company_rating, job_recommendation, ceo_approval, cat_arr, cat_rate_arr

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None, None, None, None


# Scrape Top Review Highlights (qualitative) (Step 3)
# This step shall take place after logging in and searched company so that Reviews Tab is available for clicking
def scrape_top_reviews():
    try:
        t.click('//button[contains(text(), "Show More Pros and Cons")]') # click to exapnd Top Reviews Highlights by Sentiment
        t.wait(2)

        # Initialize lists to store  headers and descriptions
        pros_header = []
        pros_description = []
        cons_header = []
        cons_description = []

        # Loop from 1 to 5 inclusive
        for i in range(1, 6):
            # Construct XPath expressions for cons headers and descriptions
            pros_description_xpath = f'//div[@class="ReviewHighlights_highlightSectionColumn__wSvkT"][1]/ul/li[{i}]'
            pros_header_xpath = pros_description_xpath + '/a[text()]'
            cons_description_xpath = f'//div[@class="ReviewHighlights_highlightSectionColumn__wSvkT"][2]/ul/li[{i}]'
            cons_header_xpath = cons_description_xpath + '/a[text()]'

            # Read cons header and description using TagUI's t.read() function
            pros_header.append(t.read(pros_header_xpath))
            pros_description.append(t.read(pros_description_xpath).split("\xa0")[0])
            cons_header.append(t.read(cons_header_xpath))
            cons_description.append(t.read(cons_description_xpath).split("\xa0")[0])
    
        return pros_header, pros_description, cons_header, cons_description

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None, None, None



# Scrape from Glassdoor - Ratings and Top Review Highlights and Competitors' Ratings
def glassdoor_scrape(email, email_pw, company):
    try:
        # Step 0 - search via google for top competitors
        top_competitors = scrape_competitors(company) 

        # Step 1 - access glassdoor and search company
#         t.init(visual_automation = True) # visual automation if keyboard automation required in subsequent code
        t.url('https://www.glassdoor.com/') # go to glassdoor website
        t.wait(3)
        try:
              t.type('//*[@id="inlineUserEmail"]',  email +'[enter]') # login with specially created email address for glassdoor access
              t.wait(3)
              t.type('//*[@id="inlineUserPassword"]',  email_pw +'[enter]') # login with specially created email address for glassdoor access
              t.wait(3)
        except:
             pass
        t.click('//*[@id="ContentNav"]//a[contains(text(),"Companies")]') # click on Companies tab to search for companies
        t.wait(3)
        t.type('//*[contains(@placeholder,"Search for a Company")]',  company +'[enter]') # search for company
        t.click('//*[contains(@data-test,"company-search-button")]') # click on search because "enter" does not work
        t.wait(3)
        t.click('//*[@data-serp-pos="0"]//h2/a') # click on top return result

        t.wait(3)
        t.click('//*[contains(@data-test, "nav-reviews")]') # Click on Reviews Tab

        # Step 2 - scrape rating of company
        company_rating, job_recommendation, ceo_approval, cat_arr, cat_rate_arr = scrape_rating()

        # Step 3 - Scrape Top Review Highlights
        pros_header, pros_description, cons_header, cons_description = scrape_top_reviews()

        # Step 4 - scrape ratings of top competitors
        # Initialize lists to store ratings, job recommendations, and CEO approvals
        comp_rating_arr = []
        comp_job_rec_arr = []
        comp_ceo_approval_arr = []

        t.wait(2)
        t.click('//*[contains(@data-test, "nav-reviews")]') # Click on Reviews Tab again to get back to the top

        # Loop from 0 to n exclusive
        n = len(top_competitors)
        for i in range(0, n):
            t.wait(2) # wait to simulate person clicking
            t.click('//*[contains(@data-test,"search-button")]') # click on search button
            t.wait(2) # wait to simulate person clicking
            t.click('//*[contains(@data-test,"clear-button")]') # click on clear button
            t.wait(2) # wait to simulate person clicking
            t.type('//*[contains(@data-test,"search-label")]', top_competitors[i] + '[enter]')
            t.wait(2) # wait to simulate person clicking
            t.click('//*[@id="SearchKeywordDefaultResults"]/li[1]') # click on first returned result button
            t.wait(2) # wait to simulate person clicking

            # Scrape rating, job recommendation, and CEO approval and append to respective lists

            t.click('//*[contains(@data-test, "nav-reviews")]') # Click on Reviews Tab
            t.wait(2)
            comp_rating, comp_job_rec, comp_ceo_approval, _, _ = scrape_rating()
            comp_rating_arr.append(comp_rating)
            comp_job_rec_arr.append(comp_job_rec)
            comp_ceo_approval_arr.append(comp_ceo_approval)

        t.click('//*[contains(@data-test, "utility-nav-dropdown")]/button[@aria-label="profile"]')
        t.click('//*[@id="UtilityNav"]/div[3]/div/div/ul[1]/li[6]/a[@data-test= "sign-out"]')
        t.close()

        return (
            company_rating, job_recommendation, ceo_approval,
            pros_header, pros_description, cons_header, cons_description,
            comp_rating_arr, comp_job_rec_arr, comp_ceo_approval_arr, top_competitors
        )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None, None, None, None, None, None, None, None, None, None


def competitor_comparison(top_competitors, company_rating, job_recommendation, ceo_approval, comp_rating, comp_job_rec, comp_ceo_approval):
    # Comparing against Competitors' Ratings
    company_rating_rank = 1
    company_job_rec_rank = 1
    company_ceo_app_rank = 1
    n = len(top_competitors)

    for i in range(0, n):
        if company_rating < comp_rating [i]:
            company_rating_rank += 1
        if job_recommendation < comp_job_rec [i]:
            company_job_rec_rank += 1
        if ceo_approval < comp_ceo_approval [i]:
            company_ceo_app_rank += 1

    return company_rating_rank, company_job_rec_rank, company_ceo_app_rank


def glassdoor_analysis(company):
    
    # Example Usage:
    email = "i2a.isa.iss@gmail.com" # for glassdoor access
    email_pw = "i2aproject" # for glassdoor access
    # company = 'apple' # specify company of interest

    (company_rating, job_recommendation, ceo_approval, pros_header, pros_description, cons_header, cons_description, comp_rating, comp_job_rec, comp_ceo_approval, top_competitors) = glassdoor_scrape(email, email_pw, company)
    (company_rating_rank, company_job_rec_rank, company_ceo_app_rank) = competitor_comparison(top_competitors, company_rating, job_recommendation, ceo_approval, comp_rating, comp_job_rec, comp_ceo_approval)
    return company_rating, job_recommendation, ceo_approval, pros_header, pros_description, cons_header, cons_description, comp_rating, comp_job_rec, comp_ceo_approval, top_competitors, company_rating_rank, company_job_rec_rank, company_ceo_app_rank