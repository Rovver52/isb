import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.ThreadLocalRandom;

public class BinaryRandom {
    public static int[] generateBinarySequence() {
        int[] sequence = new int[128];
        for (int i = 0; i < 128; i++) {
            sequence[i] = ThreadLocalRandom.current().nextInt(0, 2); // 0 или 1
        }
        return sequence;
    }

    public static void main(String[] args) {
        int[] sequence = generateBinarySequence();
        
        try (FileWriter writer = new FileWriter("sequence_java.txt")) {
            for (int num : sequence) {
                writer.write(Integer.toString(num));
                System.out.print(num); // Дополнительно выводим в консоль
            }
            System.out.println("\nПоследовательность сохранена в файл 'sequence_java.txt'");
        } catch (IOException e) {
            System.err.println("Ошибка при записи в файл: " + e.getMessage());
        }
    }
}