function fetchParentCompanies() {
    const spreadSheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadSheet.getActiveSheet();
    let range = sheet.getActiveRange();
    
    if (!range) {
      // If no range is selected, use the entire data range
      range = sheet.getDataRange();
    }
  
    const data = range.getValues();
    const startRowIndex = range.getRow();
    spreadSheet.toast(`Starting to fetch parent companies from...`, 'Info', 5);
  
    // Iterate over the rows
    for (let i = 0; i < data.length; i++) {
      const row = data[i];
  
      const accountName = row[1]; // Assuming account name is in the second column
      const accountDomain = row[2]; // Assuming account name is in the third column
      Logger.log(`Processing row ${i}: ${accountName} : ${accountDomain}`);
  
      if (accountName && !row[3] && !row[4]) { // Check if account name exists and target cells are empty
        Logger.log(`Calling ChatGPT API for account: ${accountName}`);
  
        let prompt, response;
        let success = false;
        let retryCount = 0;
        const maxRetries = 5;
        
        while (!success && retryCount < maxRetries) {
          prompt = getParentAndGUPrompt(accountName, accountDomain);
          response = callChatGPTAPI(prompt);
          if (response.statusCode === 429) {
            spreadSheet.toast(`Rate limit hit. Retrying in 2 seconds...`, 'Warning', 2);
            Utilities.sleep(2000); // Wait for 2 seconds before retrying
            retryCount++;
          } else {
            success = true;
          }
        }
        
        if (!success) {
          spreadSheet.toast(`Failed to fetch data for ${accountName} after ${maxRetries} attempts.`, 'Error', 2);
          continue;
        }
  
        // Logger.log(`Response from ChatGPT API: ${JSON.stringify(response)}`);
  
        try {
          
          const parsedResponse = parseGPTResponse(response);
          // Logger.log(`Parsed response: ${JSON.stringify(parsedResponse)}`);
  
          if (parsedResponse) {
            const rowIndex = startRowIndex + i;
            sheet.getRange(rowIndex, 4).setValue(parsedResponse.parentCompany); // Column C
            sheet.getRange(rowIndex, 5).setValue(parsedResponse.globalUltimateParentCompany); // Column D
  
            // Flush the changes to make sure they are visible immediately
            SpreadsheetApp.flush();
          }
  
        } catch (e) {
          spreadSheet.toast(`Error parsing response for account: ${accountName} - ${e}`, 'Error', 2);
          Logger.log(`Error parsing response for account: ${accountName} - ${e}`);
        }
      }
    }
  }
  
  function getParentAndGUPrompt(accountName, accountDomain) {
    return `Provide the parent company name and global ultimate parent company name for the following account: ${accountName} with the domain ${accountDomain}. 
    Please respond only with the data in the following JSON format: {"parentCompany": "Parent Company Name", "globalUltimateParentCompany": "Global Ultimate Parent Company Name"}. If you don't know the answer, just put the value UNKNOWN in the respective variable value.`;
  }
  
  
  function callChatGPTAPI(prompt) {
    const apiKey = '<openai api key>';
    const url = 'https://api.openai.com/v1/chat/completions';
  
    const options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: `Bearer ${apiKey}`
      },
      payload: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          {
            role: "system",
            content: "You are a helpful assistant."
          },
          {
            role: "user",
            content: prompt
          }
        ],
        max_tokens: 1000 // Adjust based on the expected length of the response
      })
    };
  
    const response = UrlFetchApp.fetch(url, options);
  
    return {
      getContentText: function() {
        return response.getContentText();
      },
      statusCode: response.getResponseCode()
    };
  }
  
  function parseGPTResponse(response) {
    const parsedResponse = JSON.parse(response.getContentText());
    const content = parsedResponse.choices[0].message.content;
    const jsonResponse = JSON.parse(content);
    return jsonResponse;
  }

  function onOpen() {
    const ui = SpreadsheetApp.getUi();
    ui.createMenu('Custom Scripts')
      .addItem('Fetch Parent Companies', 'fetchParentCompanies')
      .addItem('My menu option', 'myFunctionName')
      .addToUi();
  }