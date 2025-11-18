const diaryWriteService = (() => {
    const search = async (callback,search) => {
        const response = await fetch(`/api/tags?search=${search}`);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "Fetch error");
        }


        if(response.ok) {
            console.log("게시글 존재")
            const member = await response.json();
            if (callback) {
                callback(member);
            }

        } else {
            const error = await response.text()
            console.log(error);
        }

    }
    const checkFeeling = async (message) => {
        console.log( JSON.stringify({"message" :message}))
        const response = await fetch(`https://collections-differ-barely-muscles.trycloudflare.com/api/feel-check`, {
            method: 'POST',
            body: JSON.stringify({"message" :message}),
            headers: {
                'Content-Type': 'application/json'
            },
        });
        console.log(response)
        if (response.ok) {
            console.log("게시글 존재")
            const result = await response.json();
            return {"result" : result.result, "status" : response.status}

        } else {
            const error = await response.json()
            console.log(error.detail);
            return {"result" : error.detail,"status" : response.status}
        }
    }
    return {search: search, checkFeeling: checkFeeling}
})();