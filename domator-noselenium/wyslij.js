const fs = require('fs');  // Dodaj to na początku pliku

const fetchData = async () => {
  const results = JSON.parse(fs.readFileSync('/linki/otodom_links.json', 'utf8'));
  const dane = JSON.parse(fs.readFileSync('/dane/dane.json', 'utf8'));

  // Wczytanie ostatniego przetworzonego ID z pliku state.json
  let lastProcessedId = 0;
  if (fs.existsSync('state.json')) {
    lastProcessedId = JSON.parse(fs.readFileSync('state.json', 'utf8')).lastProcessedId;
  }

  // Rozpoczynanie przetwarzania od ostatniego nieprzetworzonego ID
  const remainingResults = results.slice(lastProcessedId);

  for (let result of remainingResults) {
    const { id, url } = result;

    try {
      const randomData = dane[Math.floor(Math.random() * dane.length)];

      // Zalogowanie danych, które są wysyłane
      console.log(`Sending request for ID: ${id} - URL: ${url}`);
      console.log({
        operationName: "SendMessage",
        variables: {
          name: randomData.IMIE,
          email: randomData.EMAIL,
          phone: randomData.TELEFON,
          text: randomData.losowa_wiadomosc,
          advertId: id,
          financeLead: false,
          city: "Warszawa",
          agentAccountId: null
        }
      });

      const response = await fetch("https://www.otodom.pl/api/query", {
        method: "POST",
        headers: {
          "accept": "multipart/mixed, application/graphql-response+json, application/graphql+json, application/json",
          "content-type": "application/json",
          "is-desktop": "true",
          "priority": "u=1, i",
          "re-fp-session": "",
          "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-origin",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        body: JSON.stringify({
          query: `
            mutation SendMessage($advertId: Int64!, $email: String!, $name: String!, $phone: String, $text: String!, $sendSimilar: Boolean, $financeLead: Boolean, $city: String, $utm: Utm, $leadFormType: String, $leadFormTool: String, $experiment: String, $agentAccountId: ID) {
              sendMessage(
                input: {
                  advertId: $advertId,
                  email: $email,
                  name: $name,
                  phone: $phone,
                  text: $text,
                  sendSimilar: $sendSimilar,
                  financeLead: $financeLead,
                  city: $city,
                  utm: $utm,
                  leadFormType: $leadFormType,
                  leadFormTool: $leadFormTool,
                  experiment: $experiment,
                  agentAccountId: $agentAccountId
                }
              ) {
                __typename
                ... on MessageResponse {
                  financeLeadResponse {
                    ... on SendLeadCollectorSuccess {
                      success
                      __typename
                    }
                    ... on SendLeadCollectorError {
                      error
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
              }
            }
          `,
          operationName: "SendMessage",
          variables: {
            name: randomData.IMIE,
            email: randomData.EMAIL,
            phone: randomData.TELEFON,
            text: randomData.losowa_wiadomosc,
            advertId: id,
            financeLead: false,
            city: "Warszawa",
            agentAccountId: null
          }
        }),
        mode: "cors",
        credentials: "include",
        referrer: url,
        referrerPolicy: "no-referrer-when-downgrade"
      });

      const data = await response.json();
      console.log(`ID: ${id} - URL: ${url} - Response:`, data);

      // Zapisz aktualny stan do pliku state.json
      fs.writeFileSync('state.json', JSON.stringify({ lastProcessedId: results.indexOf(result) + 1 }));

    } catch (error) {
      console.error(`Error sending data for ID: ${id} - URL: ${url}`, error);
    }

    // Add a delay to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
};

fetchData();
