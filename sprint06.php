// database/migrations/xxxx_create_pergunta_user_table.php

<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('pergunta_user', function (Blueprint $table) {
            $table->id();
            $table->foreignId('pergunta_id')->constrained()->cascadeOnDelete();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->timestamps();
            $table->unique(['pergunta_id', 'user_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('pergunta_user');
    }
};


// app/Models/Pergunta.php

use App\Models\User;

public function votos()
{
    return $this->belongsToMany(User::class)->withTimestamps();
}


// app/Models/User.php

use App\Models\Pergunta;

public function perguntasVotadas()
{
    return $this->belongsToMany(Pergunta::class, 'pergunta_user')->withTimestamps();
}


// routes/web.php

use App\Http\Controllers\PerguntaController;

Route::post('/perguntas/{pergunta}/votar', [PerguntaController::class, 'votar'])
    ->middleware('auth')
    ->name('perguntas.votar');


// app/Http/Controllers/PerguntaController.php

use App\Models\Pergunta;

public function votar(Pergunta $pergunta)
{
    $pergunta->votos()->toggle(auth()->id());

    return back()->with('status', 'Seu voto foi atualizado!');
}


// app/Http/Controllers/EventoController.php

use App\Models\Evento;

public function show(Evento $evento)
{
    $perguntas = $evento->perguntas()
        ->withCount('votos')
        ->with('votos')
        ->orderByDesc('votos_count')
        ->get();

    return view('eventos.show', [
        'evento' => $evento,
        'perguntas' => $perguntas,
    ]);
}


// resources/views/eventos/show.blade.php

@if (session('status'))
    <div style="background: #d4edda; padding: 10px; margin-bottom: 10px;">
        {{ session('status') }}
    </div>
@endif

@foreach ($perguntas as $pergunta)
    <div class="card" style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">

        <p>{{ $pergunta->texto }}</p>

        <p>Votos: {{ $pergunta->votos_count }}</p>

        <form action="{{ route('perguntas.votar', $pergunta) }}" method="POST">
            @csrf

            @auth
                @if ($pergunta->votos->contains(auth()->id()))
                    <button type="submit" style="background: green; color: white;">
                        Voce votou (clique para remover)
                    </button>
                @else
                    <button type="submit">
                        Upvote
                    </button>
                @endif
            @else
                <a href="{{ route('login') }}">Entre para votar</a>
            @endauth
        </form>

    </div>
@endforeach
