export interface FinderRequest {
    entity: string,
    site: string
}

export interface FinderResponse {
    entity: string,
    site: string,
    sentiment: number,
}