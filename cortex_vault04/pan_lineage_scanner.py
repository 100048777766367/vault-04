import json
import urllib.request

class PanLineageScanner:
    @staticmethod
    def auto_discover_ancestors(owner, current_slug):
        # Tự động sinh danh sách ứng viên tổ tiên dựa trên quy tắc đặt tên: vault, vault-01, vault-02...
        candidates = ["vault", "vault-01", "vault-01-01", "vault-02", "vault-03"]
        discovered = []

        for cand in candidates:
            if cand == current_slug: continue
            repo_path = f"{owner}/{cand}"
            url = f"https://raw.githubusercontent.com/{repo_path}/main/synapse_forward.json"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Vault04-Scanner"})
                with urllib.request.urlopen(req, timeout=2.5) as resp:
                    if resp.status == 200:
                        discovered.append(repo_path)
            except Exception: pass

        return discovered

    @staticmethod
    def harvest_all_triplets(ancestors):
        all_triplets = []
        paths = ["dist/bodhi_knowledge_graph.jsonl", "synapses/knowledge_graph.json"]
        
        for anc in ancestors:
            for branch in ["main", "master", "HEAD"]:
                for path in paths:
                    url = f"https://raw.githubusercontent.com/{anc}/{branch}/{path}"
                    try:
                        req = urllib.request.Request(url, headers={"User-Agent": "Vault04-Harvester"})
                        with urllib.request.urlopen(req, timeout=3.0) as resp:
                            if resp.status == 200:
                                text = resp.read().decode('utf-8')
                                if path.endswith(".jsonl"):
                                    for line in text.splitlines():
                                        if line.strip():
                                            t = json.loads(line.strip())
                                            t["ancestor_line"] = anc
                                            all_triplets.append(t)
                                else:
                                    d = json.loads(text)
                                    for edge in d.get("edges", []):
                                        if "--[" in edge and "]-->" in edge:
                                            l, r = edge.split("]--->" if "]--->" in edge else "]-->")
                                            s, p = l.split("--[")
                                            all_triplets.append({
                                                "subject": s.strip(),
                                                "predicate": p.strip().lower(),
                                                "object": r.strip(),
                                                "confidence": 0.95,
                                                "ancestor_line": anc
                                            })
                                break
                    except Exception: continue
        return all_triplets
