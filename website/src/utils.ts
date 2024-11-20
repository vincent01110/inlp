import { AddEntryRequest, FinderRequest, FinderResponse } from "./types"; // Adjust according to your file structure

export async function fetchValue(requestBody: FinderRequest): Promise<FinderResponse | null> {
    try {
        const response = await fetch('http://localhost:8000/sentiment', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                entity: requestBody.entity,
                site: requestBody.site
            })
        });

        if (!response.ok) {
            throw new Error("Failed to fetch sentiment");
        }

        const data: FinderResponse = await response.json();
        console.log(data)
        return data;
    } catch (error) {
        console.error("Error fetching sentiment:", error);
        return null;
    }
}

export async function addEntry(requestBody: AddEntryRequest): Promise<boolean | null> {
    try {
        const response = await fetch('http://localhost:8000/add', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                site: requestBody.site,
                text: requestBody.text
            })
        });

        if (!response.ok) {
            throw new Error("Failed to add entry");
        }

        return true;
    } catch (error) {
        console.error("Error adding entry:", error);
        return null;
    }
}
