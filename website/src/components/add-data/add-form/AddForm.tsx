import { Button } from "primereact/button";
import { FloatLabel } from "primereact/floatlabel";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from "primereact/inputtextarea";
import React, { useState } from "react";
import style from './AddForm.module.css';
import { redirect, useNavigate } from "react-router";
import { AddType } from "../../../types";
import { Message } from "primereact/message";
import { addEntry } from "../../../utils";

const AddForm = () => {
    const [site, setSite] = useState<string>('')
    const [text, setText] = useState<string>('')
    const navigate = useNavigate()
    const [error, setError] = useState<string[]>([])

    function appendError(errorText: string) {
        setError(prevState => {
            return [...prevState, errorText]
        })
    }

    function isSiteValid(): boolean {
        if (site.length >= 3 && site.length <= 50) {
            return true
        }
        appendError('Site needs to be between 3 and 50 characters')
        return false
    }

    function isTextValid(): boolean {
        if (text.length >= 30 && text.length <= 10000) {
            return true
        }
        appendError('Text needs to be between 30 and a 1000 characters')
        return false
    }

    async function add(addtype: AddType) {
        setError([])
        const siteValid = isSiteValid()
        const textValid = isTextValid()
        if (!siteValid || !textValid) {
            return
        }
        
        const resp = await addEntry({site, text})

        if (!resp) {
            appendError('Error adding entry, please try again later!')
            return
        }

        if (addtype === AddType.ADD) {
            return navigate('/')
        }
        if (addtype === AddType.ADD_AND_NEW) {
            setSite('')
            setText('')
            setError([])
            return
        }
    }

    return <div className={style.form}>
        <FloatLabel>
            <InputText id="site" minLength={3} maxLength={50} value={site} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSite(e.target.value)} />
            <label htmlFor="site">Site</label>
        </FloatLabel>
        <FloatLabel>
            <InputTextarea autoResize cols={60} rows={10} id="text" value={text} onChange={(e) => setText(e.target.value)} />
            <label htmlFor="text">Text</label>
        </FloatLabel>
        <div className={style.errorBox}>
            {error && error.map((e, i) => <Message key={i} severity="error" text={e} />)}
        </div>
        <div className={style.buttonContainer}>
            <Button label="Cancel" icon='pi pi-times' onClick={() => navigate('/')} style={{ backgroundColor: '#ff6978', borderColor: 'red', outlineColor: 'red' }} />
            <Button label="Add" icon='pi pi-check' onClick={() => add(AddType.ADD)} />
            <Button label="Add and New" icon='pi pi-plus' onClick={() => add(AddType.ADD_AND_NEW)} />
        </div>

    </div>
}

export default AddForm;