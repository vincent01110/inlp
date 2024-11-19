import { FinderRequest, FinderResponse } from "./types"; // Adjust according to your file structure

export async function fetchValue(requestBody: FinderRequest): Promise<FinderResponse | null> {
    try {
        const response = await fetch('http://localhost:8000/get_entity_sentiment', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                entity: requestBody.entity,
                site: requestBody.site,
                file_path: "./reviews.csv"
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
