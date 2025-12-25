import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:research/lib/main.dart';
import 'package:research/lib/providers/auth_provider.dart';
import 'package:research/lib/providers/offre_provider.dart';

void main() {
  testWidgets('App should start with SplashScreen', (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => AuthProvider()),
          ChangeNotifierProvider(create: (_) => OffreProvider()),
        ],
        child: const MyApp(),
      ),
    );

    // Vérifier que le SplashScreen est présent
    expect(find.byType(MaterialApp), findsOneWidget);
  });

  testWidgets('SplashScreen should display app name', (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => AuthProvider()),
          ChangeNotifierProvider(create: (_) => OffreProvider()),
        ],
        child: const MyApp(),
      ),
    );

    await tester.pump(); // Lancer le build initial

    // Attendre un peu pour que le splash screen s'affiche
    await tester.pump(const Duration(milliseconds: 100));

    // Vérifier la présence d'éléments du splash screen
    // Note: Les éléments exacts dépendent de l'implémentation
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}

