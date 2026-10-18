class HeterosisSelector:
    @staticmethod
    def select_apex_genome(recombined_triplets, threshold=0.90):
        # Tích lũy ưu thế lai: gen nào tồn tại qua nhiều đời tổ tiên thì sức sống càng mãnh liệt
        apex_map = {}
        for item in recombined_triplets:
            key = f"{item['subject']}_{item['predicate']}_{item['object']}"
            if item["confidence"] < threshold:
                continue

            if key not in apex_map:
                apex_map[key] = item
                apex_map[key]["lineage_heritage"] = [item["ancestor_line"]]
            else:
                entry = apex_map[key]
                # Tăng vọt độ tin cậy nhờ ưu thế lai qua nhiều thế hệ
                entry["confidence"] = min(0.9999, round(entry["confidence"] + 0.02, 4))
                if item["ancestor_line"] not in entry["lineage_heritage"]:
                    entry["lineage_heritage"].append(item["ancestor_line"])

        return list(apex_map.values())
