import java.util.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class BSTProgram {
    static Scanner sc = new Scanner(System.in);

    // ── NODE ─────────────────────────────
    static class Node {
        int id;
        String nama;
        Node left, right;

        Node(int id, String nama) {
            this.id = id;
            this.nama = nama;
        }
    }

    // ── BST ──────────────────────────────
    static class BST {
        Node root;

        void tambah(int id, String nama) {
            root = tambahRek(root, id, nama);
        }

        private Node tambahRek(Node node, int id, String nama) {
            if (node == null)
                return new Node(id, nama);

            if (id < node.id)
                node.left = tambahRek(node.left, id, nama);
            else if (id > node.id)
                node.right = tambahRek(node.right, id, nama);
            else
                System.out.println("  [!] ID sudah ada!");

            return node;
        }

        Node cariRek(Node node, int id) {
            if (node == null || node.id == id)
                return node;
            return id < node.id ? cariRek(node.left, id) : cariRek(node.right, id);
        }

        void cari(int id) {
            Node n = cariRek(root, id);
            if (n != null)
                System.out.println("  [v] Ditemukan: ID=" + n.id + " Nama=" + n.nama);
            else
                System.out.println("  [x] Tidak ditemukan");
        }

        void hapus(int id) {
            if (cariRek(root, id) == null) {
                System.out.println("  [!] Data tidak ada");
                return;
            }
            root = hapusRek(root, id);
            System.out.println("  [v] Data dihapus");
        }

        Node hapusRek(Node node, int id) {
            if (node == null)
                return null;

            if (id < node.id)
                node.left = hapusRek(node.left, id);
            else if (id > node.id)
                node.right = hapusRek(node.right, id);
            else {
                if (node.left == null)
                    return node.right;
                if (node.right == null)
                    return node.left;

                Node succ = min(node.right);
                node.id = succ.id;
                node.nama = succ.nama;
                node.right = hapusRek(node.right, succ.id);
            }
            return node;
        }

        Node min(Node node) {
            while (node.left != null)
                node = node.left;
            return node;
        }

        // ── TRAVERSAL + JUDUL ─────────────────

        void inorder() {
            System.out.println("\nINORDER — Kiri -> Root -> Kanan");
            inorderRek(root);
        }

        void preorder() {
            System.out.println("\nPREORDER — Root -> Kiri -> Kanan");
            preorderRek(root);
        }

        void postorder() {
            System.out.println("\nPOSTORDER — Kiri -> Kanan -> Root");
            postorderRek(root);
        }

        void tampilSemuaTraversal() {
            if (isEmpty()) {
                System.out.println("  [!] BST kosong.");
                return;
            }

            System.out.println("\n=== SEMUA TRAVERSAL ===");

            inorder();
            System.out.println();

            preorder();
            System.out.println();

            postorder();
            System.out.println();
        }

        void inorderRek(Node n) {
            if (n != null) {
                inorderRek(n.left);
                System.out.println(n.id + " - " + n.nama);
                inorderRek(n.right);
            }
        }

        void preorderRek(Node n) {
            if (n != null) {
                System.out.println(n.id + " - " + n.nama);
                preorderRek(n.left);
                preorderRek(n.right);
            }
        }

        void postorderRek(Node n) {
            if (n != null) {
                postorderRek(n.left);
                postorderRek(n.right);
                System.out.println(n.id + " - " + n.nama);
            }
        }

        boolean isEmpty() {
            return root == null;
        }
    }

    // ── IMPORT CSV ─────────────────────────
    static void importCSV(BST bst, String path) {
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(new FileInputStream(path), StandardCharsets.UTF_8))) {

            String line = br.readLine();
            if (line == null) {
                System.out.println("  [!] CSV kosong!");
                return;
            }

            String delimiter = line.contains(";") ? ";" : ",";
            String[] header = line.split(delimiter);

            int idxId = -1, idxNama = -1;

            for (int i = 0; i < header.length; i++) {
                String h = header[i].toLowerCase();
                if (h.contains("id"))
                    idxId = i;
                if (h.contains("nama"))
                    idxNama = i;
            }

            if (idxId == -1 || idxNama == -1) {
                System.out.println("  [!] Kolom tidak ditemukan!");
                return;
            }

            int berhasil = 0, gagal = 0;

            while ((line = br.readLine()) != null) {
                String[] val = line.split(delimiter);

                if (val.length <= Math.max(idxId, idxNama)) {
                    gagal++;
                    continue;
                }

                try {
                    int id = Integer.parseInt(val[idxId].trim());
                    String nama = val[idxNama].trim();

                    bst.tambah(id, nama);
                    berhasil++;
                } catch (Exception e) {
                    gagal++;
                }
            }

            System.out.println("  Berhasil: " + berhasil);
            System.out.println("  Gagal   : " + gagal);

        } catch (Exception e) {
            System.out.println("  Error: " + e.getMessage());
        }
    }

    // ── MAIN MENU ─────────────────────────
    public static void main(String[] args) {
        BST bst = new BST();

        while (true) {
            System.out.println("\n===== MENU BST =====");
            System.out.println("1. Import CSV");
            System.out.println("2. Tambah Manual");
            System.out.println("3. Cari");
            System.out.println("4. Hapus");
            System.out.println("5. Inorder");
            System.out.println("6. Preorder");
            System.out.println("7. Postorder");
            System.out.println("8. Semua Traversal");
            System.out.println("0. Keluar");
            System.out.print("Pilih: ");
            String p = sc.nextLine();

            switch (p) {
                case "1":
                    System.out.print("Path CSV: ");
                    String path = sc.nextLine();
                    importCSV(bst, path);
                    break;

                case "2":
                    System.out.print("ID: ");
                    int id = Integer.parseInt(sc.nextLine());
                    System.out.print("Nama: ");
                    String nama = sc.nextLine();
                    bst.tambah(id, nama);
                    break;

                case "3":
                    System.out.print("ID: ");
                    bst.cari(Integer.parseInt(sc.nextLine()));
                    break;

                case "4":
                    System.out.print("ID: ");
                    bst.hapus(Integer.parseInt(sc.nextLine()));
                    break;

                case "5":
                    bst.inorder();
                    break;

                case "6":
                    bst.preorder();
                    break;

                case "7":
                    bst.postorder();
                    break;

                case "8":
                    bst.tampilSemuaTraversal();
                    break;

                case "0":
                    System.out.println("Selesai.");
                    return;

                default:
                    System.out.println("Pilihan salah!");
            }
        }
    }
}