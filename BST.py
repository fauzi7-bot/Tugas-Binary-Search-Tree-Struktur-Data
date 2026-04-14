import os
import csv

# ══════════════════════════════════════════════════════════════
#   BINARY SEARCH TREE — Python (Input Manual + Import CSV)
# ══════════════════════════════════════════════════════════════

def buka_file_dialog():
    """
    Membuka jendela dialog pilih file CSV.
    Mengembalikan path file yang dipilih, atau None jika dibatalkan.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title="Pilih File CSV",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )
        root.destroy()
        return path if path else None
    except ImportError:
        return None


# ── NODE ─────────────────────────────────────────────────────────
class Node:
    def __init__(self, id, nama):
        self.id    = id
        self.nama  = nama
        self.left  = None
        self.right = None


# ── BST ──────────────────────────────────────────────────────────
class BST:
    def __init__(self):
        self.root = None

    def tambah(self, id, nama, verbose=True):
        if self.root is None:
            self.root = Node(id, nama)
            if verbose:
                print(f"  [+] Data ({id}, '{nama}') berhasil ditambahkan sebagai root.")
        else:
            self._tambah_rek(self.root, id, nama, verbose)

    def _tambah_rek(self, node, id, nama, verbose):
        if id < node.id:
            if node.left is None:
                node.left = Node(id, nama)
                if verbose:
                    print(f"  [+] Data ({id}, '{nama}') berhasil ditambahkan.")
            else:
                self._tambah_rek(node.left, id, nama, verbose)
        elif id > node.id:
            if node.right is None:
                node.right = Node(id, nama)
                if verbose:
                    print(f"  [+] Data ({id}, '{nama}') berhasil ditambahkan.")
            else:
                self._tambah_rek(node.right, id, nama, verbose)
        else:
            print(f"  [!] ID {id} sudah ada di BST. Data '{nama}' dilewati.")

    def cari(self, id):
        node = self._cari_rek(self.root, id)
        if node:
            print(f"  [v] Data ditemukan  ->  ID: {node.id}  |  Nama: '{node.nama}'")
        else:
            print(f"  [x] Data dengan ID {id} tidak ditemukan.")
        return node

    def _cari_rek(self, node, id):
        if node is None or node.id == id:
            return node
        return self._cari_rek(node.left, id) if id < node.id else self._cari_rek(node.right, id)

    def hapus(self, id):
        if self._cari_rek(self.root, id) is None:
            print(f"  [x] Data dengan ID {id} tidak ditemukan, gagal menghapus.")
            return
        self.root = self._hapus_rek(self.root, id)
        print(f"  [-] Data dengan ID {id} berhasil dihapus.")

    def _hapus_rek(self, node, id):
        if node is None:
            return node
        if id < node.id:
            node.left  = self._hapus_rek(node.left,  id)
        elif id > node.id:
            node.right = self._hapus_rek(node.right, id)
        else:
            if node.left  is None: return node.right
            if node.right is None: return node.left
            succ       = self._min_node(node.right)
            node.id    = succ.id
            node.nama  = succ.nama
            node.right = self._hapus_rek(node.right, succ.id)
        return node

    def _min_node(self, node):
        cur = node
        while cur.left:
            cur = cur.left
        return cur

    def inorder(self):
        h = []; self._inorder_rek(self.root, h); return h
    def _inorder_rek(self, n, h):
        if n: self._inorder_rek(n.left, h); h.append((n.id, n.nama)); self._inorder_rek(n.right, h)

    def preorder(self):
        h = []; self._preorder_rek(self.root, h); return h
    def _preorder_rek(self, n, h):
        if n: h.append((n.id, n.nama)); self._preorder_rek(n.left, h); self._preorder_rek(n.right, h)

    def postorder(self):
        h = []; self._postorder_rek(self.root, h); return h
    def _postorder_rek(self, n, h):
        if n: self._postorder_rek(n.left, h); self._postorder_rek(n.right, h); h.append((n.id, n.nama))

    def is_empty(self):
        return self.root is None

    def cetak(self, data, judul):
        if not data:
            print("  (BST kosong)"); return
        print(f"\n  +-------+--------+-----------------------------------+")
        print(f"  | {'No.':<5} | {'ID':^6} | {'Nama':<33} |")
        print(f"  | {judul:<52}|")
        print(f"  +-------+--------+-----------------------------------+")
        print(f"  | {'No.':<5} | {'ID':^6} | {'Nama':<33} |")
        print(f"  +-------+--------+-----------------------------------+")
        for i, (id, nama) in enumerate(data, 1):
            print(f"  | {i:>5} | {id:>6} | {nama:<33} |")
        print(f"  +-------+--------+-----------------------------------+")
        print(f"  Total: {len(data)} data")


# ══════════════════════════════════════════════════════════════
#   HELPER
# ══════════════════════════════════════════════════════════════

def baris(char="=", n=60): print(char * n)
def header(judul): baris(); print(f"  {judul}"); baris()
def clear(): os.system("cls" if os.name == "nt" else "clear")

def input_id(prompt="  Masukkan ID (angka): "):
    while True:
        try: return int(input(prompt))
        except ValueError: print("  [!] ID harus angka bulat. Coba lagi.")

def input_nama(prompt="  Masukkan Nama     : "):
    while True:
        val = input(prompt).strip()
        if val: return val
        print("  [!] Nama tidak boleh kosong. Coba lagi.")

def input_jumlah():
    while True:
        try:
            n = int(input("  Jumlah data yang ingin ditambahkan (0 = tanpa batas): "))
            if n >= 0: return n
            print("  [!] Jumlah tidak boleh negatif.")
        except ValueError:
            print("  [!] Masukkan angka bulat.")


# ══════════════════════════════════════════════════════════════
#   SUB-MENU TAMBAH DATA (CSV VERSION)
# ══════════════════════════════════════════════════════════════

def menu_tambah(bst):
    while True:
        clear()
        header("TAMBAH DATA")
        print("  [1]  Input Manual")
        print("  [2]  Import dari File CSV (.csv)")
        print("  [0]  Kembali")
        print()
        baris("-")
        pilihan = input("  Pilih cara tambah: ").strip()
        print()

        # ── MANUAL ───────────────────────────────────────────
        if pilihan == "1":
            header("TAMBAH DATA — MANUAL")
            jumlah_target = input_jumlah()
            if jumlah_target == 0:
                print("  (Tanpa batas — ketik 'selesai' pada ID untuk berhenti)\n")
            else:
                print(f"  (Akan memasukkan {jumlah_target} data)\n")

            jumlah = 0
            while True:
                if jumlah_target > 0 and jumlah >= jumlah_target:
                    print(f"\n  [v] {jumlah_target} data berhasil ditambahkan.")
                    break

                sisa      = f" ({jumlah+1}/{jumlah_target})" if jumlah_target > 0 else ""
                hint_stop = "" if jumlah_target > 0 else " / 'selesai'"
                raw       = input(f"  Masukkan ID{sisa} (angka{hint_stop}): ").strip()

                if jumlah_target == 0 and raw.lower() == "selesai":
                    print(f"\n  Total data ditambahkan: {jumlah}")
                    break
                try:
                    id = int(raw)
                except ValueError:
                    print("  [!] ID harus angka. Coba lagi.\n"); continue

                nama = input_nama()
                bst.tambah(id, nama)
                jumlah += 1
                print()

        # ── IMPORT CSV ───────────────────────────────────────
        elif pilihan == "2":
            header("TAMBAH DATA — IMPORT CSV")

            # ── Buka file dialog atau fallback ke input manual ──
            path = None
            print("  [Mencoba membuka jendela pilih file CSV...]")
            path = buka_file_dialog()
            
            if path:
                print(f"  [v] File dipilih: {path}\n")
            else:
                print("  [!] Dialog tidak tersedia, masukkan path manual.")
                print("  Contoh Windows : C:\\Users\\Anda\\Downloads\\data.csv")
                print("  Contoh Linux   : /home/user/data.csv\n")
                path = input("  Path file CSV: ").strip().strip('"').strip("'")
            
            if not os.path.exists(path):
                print(f"\n  [!] File tidak ditemukan: {path}")
                input("\n  Tekan Enter untuk kembali..."); continue
            if not path.lower().endswith('.csv'):
                print("  [!] File harus berformat .csv")
                input("\n  Tekan Enter untuk kembali..."); continue

            try:
                # ── Baca CSV ──────────────────────────────────────
                with open(path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    header_row = next(reader, None)
                    
                    if header_row is None:
                        print("  [!] File CSV kosong!")
                        input("\n  Tekan Enter untuk kembali..."); continue

                    # ── Deteksi kolom ID dan Nama ────────────────────
                    header_list = [str(h).strip().lower() for h in header_row]
                    KATA_ID   = ["id", "kode", "no", "nomor", "code"]
                    KATA_NAMA = ["nama", "name", "barang", "produk", "item"]

                    idx_id   = next((i for i, h in enumerate(header_list) if any(k in h for k in KATA_ID)),   None)
                    idx_nama = next((i for i, h in enumerate(header_list) if any(k in h for k in KATA_NAMA)), None)

                    # Tampilkan header
                    print(f"\n  Header CSV ({len(header_row)} kolom):")
                    for i, h in enumerate(header_row):
                        tag = ""
                        if i == idx_id:   tag = "  ← kolom ID"
                        if i == idx_nama: tag = "  ← kolom Nama"
                        print(f"    [{i+1}] {h}{tag}")

                    # Konfirmasi/pilih kolom manual
                    if idx_id is None or idx_nama is None:
                        print("\n  [!] Deteksi otomatis gagal. Pilih kolom manual:")
                    else:
                        print(f"\n  Deteksi: ID='{header_row[idx_id]}' | Nama='{header_row[idx_nama]}'")
                        konfirm = input("  Benar? (y/n): ").strip().lower()
                        if konfirm != 'y':
                            idx_id = idx_nama = None

                    if idx_id is None or idx_nama is None:
                        while True:
                            try:
                                idx_id   = int(input("  Nomor kolom ID   : ")) - 1
                                idx_nama = int(input("  Nomor kolom Nama : ")) - 1
                                if 0 <= idx_id < len(header_row) and 0 <= idx_nama < len(header_row):
                                    break
                                print("  [!] Nomor di luar jangkauan.")
                            except ValueError:
                                print("  [!] Masukkan angka.")

                    # ── Tanya jumlah data ───────────────────────────
                    print()
                    jumlah_target = input_jumlah()

                    # ── Import data dari CSV ─────────────────────────
                    print("\n  Mengimpor data...")
                    berhasil = gagal = 0
                    for row_num, row in enumerate(reader, 2):  # row 2 = data pertama
                        if jumlah_target > 0 and berhasil >= jumlah_target:
                            break
                            
                        if len(row) <= max(idx_id, idx_nama):
                            gagal += 1
                            continue
                            
                        try:
                            val_id = row[idx_id].strip()
                            val_nama = row[idx_nama].strip()
                            
                            if not val_id or not val_nama:
                                gagal += 1
                                continue
                                
                            id_int = int(float(val_id))  # Handle 101.0 -> 101
                            bst.tambah(id_int, val_nama)
                            berhasil += 1
                            
                        except (ValueError, IndexError):
                            gagal += 1
                            continue

                    print(f"\n  {'─'*40}")
                    print(f"  Import CSV selesai!")
                    print(f"  Berhasil: {berhasil} data")
                    print(f"  Gagal:    {gagal} data")
                    print(f"  {'─'*40}")

            except UnicodeDecodeError:
                print("  [!] Error encoding. Coba buka file dengan encoding lain.")
            except Exception as e:
                print(f"  [!] Gagal membaca CSV: {e}")

        elif pilihan == "0":
            break
        else:
            print("  [!] Pilihan tidak valid.")

        print()
        input("  Tekan Enter untuk kembali ke sub-menu tambah...")


# ══════════════════════════════════════════════════════════════
#   MAIN (Tidak berubah)
# ══════════════════════════════════════════════════════════════

def main():
    bst = BST()

    while True:
        clear()
        baris()
        print("   PROGRAM BST (BINARY SEARCH TREE) — Python")
        print("   Struktur Data | Input Manual + Import CSV")
        baris()
        print()
        print("  [1]  Tambah Data")
        print("  [2]  Cari Data")
        print("  [3]  Hapus Data")
        print("  [4]  Traversal Inorder")
        print("  [5]  Traversal Preorder")
        print("  [6]  Traversal Postorder")
        print("  [7]  Tampilkan Semua Traversal")
        print("  [0]  Keluar")
        print()
        baris("-")
        pilihan = input("  Pilih menu: ").strip()
        print()

        if   pilihan == "1": menu_tambah(bst); continue
        elif pilihan == "2":
            header("CARI DATA")
            if bst.is_empty(): print("  [!] BST masih kosong.")
            else: bst.cari(input_id())
        elif pilihan == "3":
            header("HAPUS DATA")
            if bst.is_empty(): print("  [!] BST masih kosong.")
            else: bst.hapus(input_id())
        elif pilihan == "4":
            header("TRAVERSAL INORDER")
            if bst.is_empty(): print("  [!] BST masih kosong.")
            else: bst.cetak(bst.inorder(), "INORDER — Kiri -> Root -> Kanan")
        elif pilihan == "5":
            header("TRAVERSAL PREORDER")
            if bst.is_empty(): print("  [!] BST masih kosong.")
            else: bst.cetak(bst.preorder(), "PREORDER — Root -> Kiri -> Kanan")
        elif pilihan == "6":
            header("TRAVERSAL POSTORDER")
            if bst.is_empty(): print("  [!] BST masih kosong.")
            else: bst.cetak(bst.postorder(), "POSTORDER — Kiri -> Kanan -> Root")
        elif pilihan == "7":
            header("SEMUA TRAVERSAL")
            if bst.is_empty(): print("  [!] BST masih kosong.")
            else:
                bst.cetak(bst.inorder(),   "INORDER   — Kiri -> Root -> Kanan"); print()
                bst.cetak(bst.preorder(),  "PREORDER  — Root -> Kiri -> Kanan"); print()
                bst.cetak(bst.postorder(), "POSTORDER — Kiri -> Kanan -> Root")
        elif pilihan == "0":
            baris(); print("  Program selesai. Terima kasih!"); baris(); break
        else:
            print("  [!] Pilihan tidak valid. Masukkan angka 0-7.")

        print()
        input("  Tekan Enter untuk kembali ke menu utama...")


if __name__ == "__main__":
    main()