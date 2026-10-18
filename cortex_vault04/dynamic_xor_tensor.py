import hashlib

class DynamicSuperXorTensor:
    @staticmethod
    def recombine_n_power_n(triplets, num_ancestors):
        # Không gian hoán vị N^N co giãn động theo số lượng tổ tiên tìm được
        n_dim = max(2, min(num_ancestors, 8))
        recombined = []

        for i, t in enumerate(triplets):
            s = str(t.get("subject", "")).strip().capitalize()
            p = str(t.get("predicate", "")).strip().lower().replace(" ", "_")
            o = str(t.get("object", "")).strip().capitalize()
            anc = str(t.get("ancestor_line", "root"))

            # Băm bọt biển hoán vị Siêu XOR
            seed = f"{s}_{p}_{o}_{anc}_{i}_{n_dim}".encode()
            masks = [int(hashlib.shake_256(f"{seed}_{d}".encode()).hexdigest(2), 16) / 255.0 for d in range(n_dim)]
            xor_factor = sum(masks) / len(masks)
            
            # Điều biến độ tin cậy qua hoán vị N^N
            base_conf = float(t.get("confidence", 0.95))
            blended_conf = min(0.9999, round(base_conf * 0.85 + (xor_factor * 0.15), 4))

            recombined.append({
                "subject": s,
                "predicate": p,
                "object": o,
                "confidence": blended_conf,
                "ancestor_line": anc,
                "xor_n_signature": hashlib.shake_256(seed).hexdigest(12)
            })
        return recombined
