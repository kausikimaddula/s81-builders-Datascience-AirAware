import { useEffect, useState } from "react";
import { downloadCleanedData, getCleanedData } from "../services/api";

const PAGE_SIZE = 10;

function DataTablePage() {
  const [rows, setRows] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [area, setArea] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getCleanedData({
          search: search || undefined,
          category: category || undefined,
          area: area || undefined,
          page,
          page_size: PAGE_SIZE,
        });
        setRows(data.data || []);
        setTotal(data.total || 0);
      } catch {
        setRows([]);
        setTotal(0);
      }
    };

    fetchData();
  }, [search, category, area, page]);

  useEffect(() => {
    setPage(1);
  }, [search, category, area]);

  return (
    <section className="space-y-5">
      <div className="rounded-2xl border border-ink/10 bg-white p-5 shadow-soft">
        <div className="grid gap-3 md:grid-cols-4">
          <input
            type="text"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search issue/category/area"
            className="rounded-xl border border-ink/10 px-3 py-2 text-sm"
          />
          <input
            type="text"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
            placeholder="Filter category"
            className="rounded-xl border border-ink/10 px-3 py-2 text-sm"
          />
          <input
            type="text"
            value={area}
            onChange={(event) => setArea(event.target.value)}
            placeholder="Filter area"
            className="rounded-xl border border-ink/10 px-3 py-2 text-sm"
          />
          <a
            href={downloadCleanedData()}
            className="inline-flex items-center justify-center rounded-xl bg-ocean px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700"
          >
            Download CSV
          </a>
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-ink/10 bg-white shadow-soft">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-mist text-slate">
              <tr>
                <th className="px-4 py-3 font-semibold">Issue</th>
                <th className="px-4 py-3 font-semibold">Category</th>
                <th className="px-4 py-3 font-semibold">Area</th>
                <th className="px-4 py-3 font-semibold">Date</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row, idx) => (
                <tr key={`${row.source_row}-${idx}`} className="border-b border-ink/10">
                  <td className="px-4 py-3">{row.issue}</td>
                  <td className="px-4 py-3 capitalize">{row.category}</td>
                  <td className="px-4 py-3">{row.area}</td>
                  <td className="px-4 py-3">{row.date}</td>
                </tr>
              ))}
              {rows.length === 0 && (
                <tr>
                  <td className="px-4 py-4 text-slate" colSpan={4}>
                    No cleaned records found yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="flex items-center justify-between border-t border-ink/10 px-4 py-3 text-sm text-slate">
          <p>
            Showing {rows.length} of {total} records
          </p>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              className="rounded-lg border border-ink/10 px-3 py-1.5 hover:bg-mist"
            >
              Prev
            </button>
            <span>
              Page {page} / {totalPages}
            </span>
            <button
              type="button"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              className="rounded-lg border border-ink/10 px-3 py-1.5 hover:bg-mist"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export default DataTablePage;
