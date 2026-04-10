import axios from "axios";
import { useState } from "react";

function Upload() {
  const [loading, setLoading] = useState(false);

  const uploadFiles = async (e) => {
    const files = e.target.files;
    console.log("Selected files:", files.length);
    for (let i = 0; i < files.length; i++) {
      console.log(`File ${i}: ${files[i].name}, size: ${files[i].size}`);
    }

    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    console.log("FormData created, sending to backend...");

    try {
      setLoading(true);
      console.log("Uploading...");

      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("SUCCESS:", res.data);
      alert("Upload successful ✅");

    } catch (error) {
      console.error("UPLOAD ERROR:", error);
      console.error("Error response:", error.response?.data);
      alert("Upload failed ❌ Check console for details");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Resumes</h2>

      <input type="file" multiple onChange={uploadFiles} />

      {loading && <p>Uploading...</p>}
    </div>
  );
}

export default Upload;