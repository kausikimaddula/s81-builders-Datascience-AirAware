import { useEffect, useMemo, useState } from "react";
import LoadingBar from "../components/LoadingBar";
import {
  getMappings,
  getProgress,
  predictCategories,
  scanDuplicates,
  trainModel,
  updateMappings,
  uploadFile,
} from "../services/api";

function parsePreview(file) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const text = String(reader.result || "");
        if (file.name.toLowerCase().endsWith(".json")) {
          const parsed = JSON.parse(text);
          const records = Array.isArray(parsed) ? parsed : [parsed];
          resolve(records.slice(0, 5));
          return;
        }

        const [headerLine, ...rows] = text.split(/\r?\n/).filter(Boolean);
        if (!headerLine) {
          resolve([]);
          return;
        }
        const headers = headerLine.split(",").map((h) => h.trim());
        const preview = rows.slice(0, 5).map((line) => {
          const values = line.split(",");
          return headers.reduce((acc, key, index) => {
            acc[key] = (values[index] || "").trim();
            return acc;
          }, {});
        });
        resolve(preview);
      } catch {
        resolve([]);
      }
    };
    reader.readAsText(file);
  });
}

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [rawPreview, setRawPreview] = useState([]);
  const [apiPreview, setApiPreview] = useState([]);
  const [status, setStatus] = useState("");
  const [isCleaning, setIsCleaning] = useState(false);
  const [progress, setProgress] = useState({ percent: 0, stage: "idle" });
  const [mappingText, setMappingText] = useState("");
  const [duplicatePairs, setDuplicatePairs] = useState([]);
  const [mlStatus, setMlStatus] = useState("");
  const [predictText, setPredictText] = useState("");
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const loadMappings = async () => {
      try {
        const data = await getMappings();
        setMappingText(JSON.stringify(data.category_mapping, null, 2));
      } catch {
        setMappingText('{}');
      }
    };
    loadMappings();
  }, []);

  useEffect(() => {
    if (!isCleaning) return undefined;

    const interval = setInterval(async () => {
      try {
        const data = await getProgress();
        setProgress(data);
      } catch {
        // Silent polling failure handling to keep UI responsive.
      }
    }, 450);

    return () => clearInterval(interval);
  }, [isCleaning]);

  const previewColumns = useMemo(() => {
    const first = rawPreview[0] || apiPreview[0];
    return first ? Object.keys(first) : [];
  }, [rawPreview, apiPreview]);

  const onFileChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setSelectedFile(file);
    setStatus("");
    const preview = await parsePreview(file);
    setRawPreview(preview);
    setApiPreview([]);
  };

  const onCleanData = async () => {
    if (!selectedFile) {
      setStatus("Please choose a CSV or JSON file first.");
      return;
    }

    try {
      setIsCleaning(true);
      setProgress({ percent: 5, stage: "Starting" });
      const result = await uploadFile(selectedFile);
      setApiPreview(result.preview || []);
      setStatus(`Cleaned ${result.cleaned_rows} rows from ${result.raw_rows} uploaded rows.`);
      setProgress({ percent: 100, stage: "Completed" });
    } catch (error) {
      setStatus(error?.response?.data?.detail || "Cleaning failed. Please check file format.");
      setProgress({ percent: 0, stage: "failed" });
    } finally {
      setIsCleaning(false);
    }
  };

  const onSaveMappings = async () => {
    try {
      const parsed = JSON.parse(mappingText);
      await updateMappings(parsed);
      setStatus("Category mappings updated successfully.");
    } catch {
      setStatus("Invalid mapping JSON. Please provide a valid object.");
    }
  };

  const onScanDuplicates = async () => {
    try {
      const data = await scanDuplicates({ threshold: 0.88, max_pairs: 12 });
      setDuplicatePairs(data.pairs || []);
      setStatus(`Found ${data.count || 0} potential duplicate pairs.`);
    } catch (error) {
      setStatus(error?.response?.data?.detail || "Duplicate scan failed.");
    }
  };

  const onTrainModel = async () => {
    try {
      const data = await trainModel();
      setMlStatus(
        `Model trained on ${data.trained_rows} rows across ${data.unique_categories} categories.`
      );
    } catch (error) {
      setMlStatus(error?.response?.data?.detail || "Model training failed.");
    }
  };

  const onPredictCategories = async () => {
    const issues = predictText
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);

    if (!issues.length) {
      setMlStatus("Enter one issue per line to predict categories.");
      return;
    }

    try {
      const data = await predictCategories(issues);
      setPredictions(data.predictions || []);
      setMlStatus(`Generated ${data.predictions?.length || 0} predictions.`);
    } catch (error) {
      setMlStatus(error?.response?.data?.detail || "Prediction failed.");
    }
  };

  return (
    <section className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
          <h2 className="font-display text-2xl font-bold text-ink">Upload Complaint Data</h2>
          <p className="mt-1 text-sm text-slate">Upload raw NGO complaint data in CSV or JSON format.</p>

          <input
            type="file"
            accept=".csv,.json"
            onChange={onFileChange}
            className="mt-4 w-full rounded-xl border border-dashed border-slate/40 p-4 text-sm"
          />

          <button
            type="button"
            onClick={onCleanData}
            disabled={isCleaning}
            className="mt-4 rounded-xl bg-coral px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-orange-500 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isCleaning ? "Cleaning..." : "Clean Data"}
          </button>

          <p className="mt-3 text-sm text-slate">{status}</p>
        </div>

        <LoadingBar percent={progress.percent} stage={progress.stage} />
      </div>

      <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
        <h3 className="font-display text-xl font-semibold text-ink">Edit Category Mappings (Bonus)</h3>
        <p className="mt-1 text-sm text-slate">Adjust issue text to normalized category mapping.</p>
        <textarea
          className="mt-4 h-48 w-full rounded-xl border border-ink/10 p-3 font-mono text-sm"
          value={mappingText}
          onChange={(event) => setMappingText(event.target.value)}
        />
        <button
          type="button"
          onClick={onSaveMappings}
          className="mt-3 rounded-xl bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-teal-700"
        >
          Save Mappings
        </button>
      </div>

      <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
        <h3 className="font-display text-xl font-semibold text-ink">Smart Duplicate Review (Bonus)</h3>
        <p className="mt-1 text-sm text-slate">Scan cleaned records for likely duplicate issue pairs.</p>
        <button
          type="button"
          onClick={onScanDuplicates}
          className="mt-4 rounded-xl bg-ink px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate"
        >
          Scan Duplicates
        </button>

        <div className="mt-4 space-y-2">
          {duplicatePairs.map((pair) => (
            <div key={`${pair.index_a}-${pair.index_b}`} className="rounded-lg border border-ink/10 p-3">
              <p className="text-sm font-semibold text-ink">{pair.issue_a}</p>
              <p className="text-sm text-slate">{pair.issue_b}</p>
              <p className="mt-1 text-xs text-slate">
                {pair.area} | {pair.date} | similarity: {pair.similarity}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
        <h3 className="font-display text-xl font-semibold text-ink">ML Auto Categorization (Bonus)</h3>
        <p className="mt-1 text-sm text-slate">Train a lightweight text model on cleaned complaints and predict categories.</p>

        <div className="mt-4 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={onTrainModel}
            className="rounded-xl bg-ocean px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-teal-700"
          >
            Train Model
          </button>
          <button
            type="button"
            onClick={onPredictCategories}
            className="rounded-xl bg-coral px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-orange-500"
          >
            Predict Categories
          </button>
        </div>

        <textarea
          className="mt-4 h-32 w-full rounded-xl border border-ink/10 p-3 text-sm"
          value={predictText}
          onChange={(event) => setPredictText(event.target.value)}
          placeholder={"Enter one complaint issue per line\nwater tanker delayed\nstreet light not working"}
        />

        <p className="mt-2 text-sm text-slate">{mlStatus}</p>

        <div className="mt-3 space-y-2">
          {predictions.map((item, idx) => (
            <div key={`${item.issue}-${idx}`} className="rounded-lg border border-ink/10 p-3 text-sm">
              <p className="font-medium text-ink">{item.issue}</p>
              <p className="text-slate">
                Predicted: <span className="font-semibold capitalize text-ink">{item.predicted_category}</span>
                {" "}
                ({Math.round((item.confidence || 0) * 100)}%)
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
        <h3 className="font-display text-xl font-semibold text-ink">Raw Data Preview</h3>
        <p className="mt-1 text-sm text-slate">Showing first 5 rows.</p>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-mist text-slate">
              <tr>
                {previewColumns.map((col) => (
                  <th key={col} className="px-3 py-2 font-semibold">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(apiPreview.length ? apiPreview : rawPreview).map((row, idx) => (
                <tr key={idx} className="border-b border-ink/10">
                  {previewColumns.map((col) => (
                    <td key={`${idx}-${col}`} className="px-3 py-2 text-slate">
                      {String(row[col] ?? "")}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

export default UploadPage;
