import AddForm from './add-form/AddForm';
import style from './AddPage.module.css';

const AddPage = () => {

    return <div className={style.container}>
        <h1>Add Data</h1>
        <AddForm />
    </div>
}

export default AddPage;