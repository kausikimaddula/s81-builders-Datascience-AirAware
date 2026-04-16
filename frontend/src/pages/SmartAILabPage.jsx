import { useState } from "react";
import { imputeComplaint, predictCategories, scanDuplicates, trainModel } from "../services/api";

function SmartAILabPage() {
  const [duplicateThreshold, setDuplicateThreshold] = useState(0.85);
  const [duplicateStatus, setDuplicateStatus] = useState("");
  const [duplicatePairs, setDuplicatePairs] = useState([]);
  const [trainStatus, setTrainStatus] = useState("");
  const [predictionInput, setPredictionInput] = useState("");
  const [predictions, setPredictions] = useState([]);
  const [imputeForm, setImputeForm] = useState({ issue: "", area: "", date: "" });
  const [imputeResult, setImputeResult] = useState(null);
  const [imputeStatus, setImputeStatus] = useState("");

  const onTrain = async () => {
    try {
      const data = await trainModel();
      setTrainStatus(
        `Model trained on ${data.trained_rows} rows with ${data.category_labels} categories and ${data.area_labels} areas.`
      );
    } catch (error) {
      setTrainStatus(error?.response?.data?.detail || "Training failed.");
    }
  };

  const onScanDuplicates = async () => {
    try {
      const data = await scanDuplicates({ threshold: Number(duplicateThreshold), max_pairs: 20 });
      setDuplicatePairs(data.pairs || []);
      setDuplicateStatus(`Found ${data.count || 0} likely duplicate pairs.`);
    } catch (error) {
      setDuplicateStatus(error?.response?.data?.detail || "Duplicate scan failed.");
    }
  };

  const onPredictCategories = async () => {
    const issues = predictionInput
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);

    if (!issues.length) {
      setTrainStatus("Enter one complaint per line first.");
      return;
    }

    try {
      const data = await predictCategories(issues);
      setPredictions(data.predictions || []);
      setTrainStatus(`Generated ${data.predictions?.length || 0} category predictions.`);
    } catch (error) {
      setTrainStatus(error?.response?.data?.detail || "Prediction failed.");
    }
  };

  const onImpute = async () => {
    if (!imputeForm.issue.trim()) {
      setImputeStatus("Issue text is required.");
      return;
    }

    try {
      const data = await imputeComplaint(imputeForm);
      setImputeResult(data.result);
      setImputeStatus("Missing value prediction completed.");
    } catch (error) {
      setImputeStatus(error?.response?.data?.detail || "Imputation failed.");
    }
  };

  return (
    <section className="space-y-6">
      <div className="rounded-3xl border border-ink/10 bg-gradient-to-br from-white to-mist/40 p-6 shadow-soft">
        <p className="text-sm font-semibold uppercase tracking-[0.22em] text-ocean">AI Lab</p>
        <h1 className="mt-2 font-display text-3xl font-bold text-ink">Smart NGO Data Cleaning & Analytics System</h1>
        <p className="mt-2 max-w-3xl text-sm text-slate">
          Train the classification model, scan for duplicate complaints, and run complaint-level
          imputation for missing category or area values.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
          <h2 className="font-display text-xl font-semibold text-ink">Duplicate Detection</h2>
          <p className="mt-1 text-sm text-slate">TF-IDF cosine similarity over complaint text.</p>
          <div className="mt-4 flex flex-wrap gap-3">
            <input
              type="number"
              min="0.5"
              max="0.99"
              step="0.01"
              value={duplicateThreshold}
              onChange={(event) => setDuplicateThreshold(event.target.value)}
              className="w-32 rounded-xl border border-ink/10 px-3 py-2 text-sm"
            />
            <button
              type="button"
              onClick={onScanDuplicates}
              className="rounded-xl bg-ink px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate"
            >
              Scan Duplicates
            </button>
          </div>
          <p className="mt-3 text-sm text-slate">{duplicateStatus}</p>
          <div className="mt-4 space-y-2">
            {duplicatePairs.map((pair) => (
              <div key={`${pair.index_a}-${pair.index_b}`} className="rounded-xl border border-ink/10 p-3 text-sm">
                <p className="font-medium text-ink">{pair.issue_a}</p>
                <p className="text-slate">{pair.issue_b}</p>
                <p className="mt-1 text-xs text-slate">
                  {pair.area} | {pair.date} | similarity {pair.similarity}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
          <h2 className="font-display text-xl font-semibold text-ink">Auto Categorization</h2>
          <p className="mt-1 text-sm text-slate">Predict categories from complaint text.</p>
          <div className="mt-4 flex gap-3">
            <button
              type="button"
              onClick={onTrain}
              className="rounded-xl bg-ocean px-5 py-2.5 text-sm font-semibold text-white hover:bg-teal-700"
            >
              Train Model
            </button>
            <button
              type="button"
              onClick={onPredictCategories}
              className="rounded-xl bg-coral px-5 py-2.5 text-sm font-semibold text-white hover:bg-orange-500"
            >
              Predict
            </button>
          </div>

          <textarea
            className="mt-4 h-36 w-full rounded-xl border border-ink/10 p-3 text-sm"
            value={predictionInput}
            onChange={(event) => setPredictionInput(event.target.value)}
            placeholder="Enter one issue per line\nno water available\nstreet light not working"
          />
          <p className="mt-3 text-sm text-slate">{trainStatus}</p>
          <div className="mt-4 space-y-2">
            {predictions.map((item, idx) => (
              <div key={`${item.issue}-${idx}`} className="rounded-xl border border-ink/10 p-3 text-sm">
                <p className="font-medium text-ink">{item.issue}</p>
                <p className="text-slate">
                  Category: <span className="font-semibold capitalize text-ink">{item.predicted_category}</span>
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
          <h2 className="font-display text-xl font-semibold text-ink">Missing Value Prediction</h2>
          <p className="mt-1 text-sm text-slate">
            Predict missing category or area for a complaint using the trained ML models.
          </p>
          <div className="mt-4 grid gap-3">
            <textarea
              className="h-28 w-full rounded-xl border border-ink/10 p-3 text-sm"
              value={imputeForm.issue}
              onChange={(event) => setImputeForm((prev) => ({ ...prev, issue: event.target.value }))}
              placeholder="Complaint issue"
            />
            <input
              type="text"
              value={imputeForm.area}
              onChange={(event) => setImputeForm((prev) => ({ ...prev, area: event.target.value }))}
              placeholder="Area (optional)"
              className="rounded-xl border border-ink/10 px-3 py-2 text-sm"
            />
            <input
              type="text"
              value={imputeForm.date}
              onChange={(event) => setImputeForm((prev) => ({ ...prev, date: event.target.value }))}
              placeholder="Date (optional, DD/MM/YY or YYYY-MM-DD)"
              className="rounded-xl border border-ink/10 px-3 py-2 text-sm"
            />
            <button
              type="button"
              onClick={onImpute}
              className="w-fit rounded-xl bg-ink px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate"
            >
              Predict Missing Values
            </button>
          </div>
          <p className="mt-3 text-sm text-slate">{imputeStatus}</p>
        </div>

        <div className="rounded-2xl border border-ink/10 bg-white p-6 shadow-soft">
          <h2 className="font-display text-xl font-semibold text-ink">Prediction Result</h2>
          <p className="mt-1 text-sm text-slate">Returned fields from the frontend-driven imputation call.</p>
          <div className="mt-4 rounded-2xl bg-mist/50 p-4 text-sm text-slate">
            {imputeResult ? (
              <pre className="whitespace-pre-wrap break-words font-mono text-xs text-ink">
                {JSON.stringify(imputeResult, null, 2)}
              </pre>
            ) : (
              <p>Run a prediction to see the filled category and area here.</p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

export default SmartAILabPage;