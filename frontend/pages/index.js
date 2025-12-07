import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [resultUrl, setResultUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please upload an image");

    setLoading(true);
    const fd = new FormData();
    fd.append("file", file);

    const r = await fetch("http://localhost:8000/api/process", {
      method: "POST",
      body: fd,
    });

    if (!r.ok) {
      setLoading(false);
      return alert("Processing failed");
    }

    const blob = await r.blob();
    setResultUrl(URL.createObjectURL(blob));
    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Pickabook Personalisation</h1>

      <form onSubmit={submit}>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files[0])} />
        <button>Upload</button>
      </form>

      {loading && <p>Processing...</p>}

      {resultUrl && (
        <div>
          <h2>Result</h2>
          <img src={resultUrl} style={{ maxWidth: "300px" }} />
        </div>
      )}
    </div>
  );
}
