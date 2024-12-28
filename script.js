fetch('/run_script')
    .then(response => {
        if (!response.ok) {
            throw new Error(HTTP error! Status: ${response.status});
        }
        return response.json();
    })
    .then(data => {
        console.log(data);  // Debug API response in the console
        
        if (data.error) {
            document.getElementById('result').innerHTML = <p class="error">Error: ${data.error}</p>;
        } else {
            document.getElementById('result').innerHTML = 
                <h2>Trending Topics</h2>
                <p>These are the most happening topics as on ${data.end_time}:</p>
                <ul>
                    ${data.trend1 ? <li>${data.trend1}</li> : ''}
                    ${data.trend2 ? <li>${data.trend2}</li> : ''}
                    ${data.trend3 ? <li>${data.trend3}</li> : ''}
                    ${data.trend4 ? <li>${data.trend4}</li> : ''}
                    ${data.trend5 ? <li>${data.trend5}</li> : ''}
                </ul>
                <p>The IP address used for this query was ${data.ip_address}.</p>
            ;
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        document.getElementById('result').innerHTML = <p class="error">Error: ${error.message}</p>;
    });


   
    const browser = await puppeteer.launch({
        headless: false,
      });
      

      try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.goto('https://example.com');
        // More operations...
        await browser.close();
      } catch (error) {
        console.error('An error occurred:', error);
      }
      

      fetch('http://127.0.0.1:5000/run_script')


