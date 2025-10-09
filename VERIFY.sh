#!/bin/bash
# Script de verificación del repositorio CV

echo "════════════════════════════════════════════════════════════════"
echo "    🔍 VERIFICACIÓN DE PROTECCIONES"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Verificar archivos protegidos
echo "🔒 Archivos protegidos (deben ser -r--r--r--):"
ls -l EN_NicolasFredes_CV.pdf compare_pdf.py 2>/dev/null | awk '{print "   " $1 " " $9}'
echo ""

# Verificar archivos modificables
echo "✏️  Archivos modificables (deben ser -rw-r--r--):"
ls -l generate_cv_from_python.py 2>/dev/null | awk '{print "   " $1 " " $9}'
echo ""

# Verificar documentación
echo "📚 Documentación:"
for file in README.md QUICK_START.md PROTECTED_FILES.txt LICENSE; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (faltante)"
    fi
done
echo ""

# Verificar dependencias
echo "📦 Verificando dependencias Python..."
if python3 -c "import reportlab, fitz, numpy" 2>/dev/null; then
    echo "   ✅ Todas las dependencias instaladas"
else
    echo "   ❌ Faltan dependencias. Ejecuta: pip install -r requirements.txt"
fi
echo ""

# Verificar sistema funcional
echo "🔧 Verificando sistema..."
if [ -f "compare_pdf.py" ] && [ -f "EN_NicolasFredes_CV.pdf" ] && [ -f "generated.pdf" ]; then
    echo "   ✅ Sistema completo"
else
    echo "   ⚠️  Archivos faltantes. Genera PDF primero: python3 generate_cv_from_python.py"
fi
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "    ✅ Verificación completa"
echo "════════════════════════════════════════════════════════════════"
