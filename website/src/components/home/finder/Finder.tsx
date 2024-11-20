import { InputText } from "primereact/inputtext"
import { FloatLabel } from "primereact/floatlabel"
import { Button } from 'primereact/button'
import React, { useState } from "react"
import "primereact/resources/themes/vela-purple/theme.css";
import style from "./Finder.module.css"
import { fetchValue } from "../../../utils";

interface FinderProps {
    show: (value?: number) => void;
}

const Finder = ({show}: FinderProps) => {
    const [site, setSite] = useState<string>("")
    const [entity, setEntity] = useState<string>("")
    const [loading, setLoading] = useState<boolean>(false)
  
    const getValue = async () => {
        try {
            const resp = await fetchValue({site, entity})
            if (resp && resp.sentiment > -1) {
                console.log(resp.sentiment)
                show(resp.sentiment)
            } else {
                show(-1)
            }
        } catch (err) {
            show(-1)
        }
    }

    const load = () => {
        setLoading(true);

        setTimeout(async () => {
            setLoading(false);
            await getValue()
        }, 2000);
    };

    return <div className={style.card}>
        <FloatLabel>
            <InputText id="site" value={site} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSite(e.target.value)} />
            <label htmlFor="site">Site</label>
        </FloatLabel>
        <FloatLabel>
            <InputText id="entity" value={entity} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEntity(e.target.value)} />
            <label htmlFor="entity">Entity</label>
        </FloatLabel>
        <Button label="Find" icon="pi pi-search" loading={loading} onClick={load} />
    </div>
}

export default Finder;