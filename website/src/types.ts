export interface FinderRequest {
    entity: string,
    site: string
}

export interface FinderResponse {
    entity: string,
    site: string,
    sentiment: number,
}

export interface AddEntryRequest {
    site: string,
    text: string
}

export interface AddEntryResponse {
    message: string
}

export enum AddType {
    ADD,
    ADD_AND_NEW
}